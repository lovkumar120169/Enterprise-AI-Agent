import json
import os
from typing import Any

from backend.agent.state import AgentState
from backend.guardrails.input import InputGuardrail
from backend.guardrails.output import OutputGuardrail
from backend.llm.bedrock import BedrockClient
from backend.llm.prompts import SYSTEM_PROMPT
from backend.tools.registry import (
    TOOL_DEFINITIONS,
    TOOL_FUNCTIONS
)
from backend.reliability.circuit_breaker import (
    CircuitBreaker
)
from backend.reliability.timeout import (
    run_with_timeout
)
from backend.utils.logging import logger


class AIAgent:

    def __init__(self):

        self.llm = BedrockClient()

        self.input_guardrail = (
            InputGuardrail()
        )

        self.output_guardrail = (
            OutputGuardrail()
        )

        self.max_iterations = int(
            os.getenv(
                "MAX_AGENT_ITERATIONS",
                "5"
            )
        )

        self.tool_timeout = float(
            os.getenv(
                "TOOL_TIMEOUT_SECONDS",
                "8"
            )
        )

        self.circuit_breakers = {
            tool_name: CircuitBreaker()
            for tool_name in TOOL_FUNCTIONS
        }

    def run(
        self,
        user_message: str,
        history: list[dict[str, Any]] | None = None
    ) -> AgentState:

        logger.info(
            "========== AGENT START =========="
        )


        state = AgentState(
            user_message=user_message
        )

        history = history or []

        # -------------------------------------------------
        # INPUT GUARDRAIL
        # -------------------------------------------------

        logger.info(
            "REQUEST → INPUT GUARDRAIL"
        )

        input_result = (
            self.input_guardrail.check(
                user_message
            )
        )

        if input_result["allowed"]:

            logger.info(
                "INPUT GUARDRAIL → PASSED → AGENT"
            )

        else:

            logger.warning(
                "INPUT GUARDRAIL → BLOCKED → REQUEST STOPPED"
            )

        

        if not input_result["allowed"]:

            state.blocked = True

            state.response = (
                "I can't process that request."
            )

            return state

        # -------------------------------------------------
        # INITIAL MESSAGE
        # -------------------------------------------------

        messages = list(history)

        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "text": user_message
                    }
                ]
            }
        )

        # -------------------------------------------------
        # AGENT LOOP
        # -------------------------------------------------

        for iteration in range(
            self.max_iterations
        ):

            logger.info(
                "AGENT | iteration=%s/%s",
                state.iterations,
                self.max_iterations
            )
            
            state.iterations = iteration + 1

            logger.info(
                "Agent iteration=%s",
                state.iterations
            )

            try:

                response = self.llm.converse(
                    messages=messages,
                    system_prompt=SYSTEM_PROMPT,
                    tools=TOOL_DEFINITIONS
                )

            except Exception as error:

                logger.exception(
                    "LLM failure"
                )

                state.error = str(error)

                state.response = (
                    "The AI service is temporarily "
                    "unavailable. Please try again."
                )

                return state

            output_message = response[
                "output"
            ][
                "message"
            ]

            stop_reason = response.get(
                "stopReason"
            )

            messages.append(
                output_message
            )

            # -------------------------------------------------
            # NORMAL FINAL RESPONSE
            # -------------------------------------------------

            if stop_reason != "tool_use":

                text = self._extract_text(
                    output_message
                )

                return self._apply_output_guardrail(
                    state,
                    text
                )

            # -------------------------------------------------
            # TOOL CALLS
            # -------------------------------------------------

            tool_results = []

            for block in output_message.get(
                "content",
                []
            ):

                if "toolUse" not in block:

                    continue

                tool_use = block[
                    "toolUse"
                ]

                tool_name = tool_use[
                    "name"
                ]

                tool_use_id = tool_use[
                    "toolUseId"
                ]

                tool_input = tool_use.get(
                    "input",
                    {}
                )

                state.selected_tool = (
                    tool_name
                )

                state.tool_calls.append(
                    {
                        "tool": tool_name,
                        "input": tool_input
                    }
                )

                logger.info(
                    "Tool selected=%s input=%s",
                    tool_name,
                    tool_input
                )

                result = (
                    self._execute_tool(
                        tool_name,
                        tool_input
                    )
                )

                tool_results.append(
                    {
                        "toolResult": {
                            "toolUseId": tool_use_id,

                            "content": [
                                {
                                    "json": result
                                }
                            ]
                        }
                    }
                )

            if not tool_results:

                return self._apply_output_guardrail(
                    state,
                    self._extract_text(
                        output_message
                    )
                )

            messages.append(
                {
                    "role": "user",
                    "content": tool_results
                }
            )

        # -------------------------------------------------
        # MAX ITERATION FALLBACK
        # -------------------------------------------------

        state.error = (
            "Maximum agent iterations reached."
        )

        state.response = (
            "I couldn't complete that request "
            "within the allowed number of steps."
        )

        return state

    def _execute_tool(
        self,
        tool_name: str,
        tool_input: dict
    ) -> dict:

        function = TOOL_FUNCTIONS.get(
            tool_name
        )

        if function is None:

            return {
                "success": False,
                "error": (
                    f"Unknown tool: {tool_name}"
                )
            }

        breaker = (
            self.circuit_breakers[
                tool_name
            ]
        )

        try:

            breaker.before_call()

            result = run_with_timeout(
                function,
                self.tool_timeout,
                **tool_input
            )

            breaker.record_success()

            return {
                "success": True,
                "data": result
            }

        except Exception as error:

            breaker.record_failure()

            logger.exception(
                "Tool failure: %s",
                tool_name
            )

            return {
                "success": False,
                "error": str(error)
            }

    @staticmethod
    def _extract_text(
        message: dict
    ) -> str:

        text_parts = []

        for block in message.get(
            "content",
            []
        ):

            if "text" in block:

                text_parts.append(
                    block["text"]
                )

        return "\n".join(
            text_parts
        ).strip()

    def _apply_output_guardrail(
        self,
        state: AgentState,
        text: str
    ) -> AgentState:

        guardrail_result = (
            self.output_guardrail.check(
                text
            )
        )

        if not guardrail_result[
            "allowed"
        ]:

            state.blocked = True

            state.response = (
                "I can't provide that response."
            )

            return state

        state.response = (
            guardrail_result["text"]
        )

        return state
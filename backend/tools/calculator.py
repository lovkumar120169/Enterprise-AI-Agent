import ast
import operator

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _evaluate(node):

    if isinstance(node, ast.Constant):

        if isinstance(
            node.value,
            (int, float)
        ):

            return node.value

        raise ValueError(
            "Only numbers are allowed."
        )

    if isinstance(node, ast.BinOp):

        operator_function = (
            _ALLOWED_OPERATORS.get(
                type(node.op)
            )
        )

        if operator_function is None:
            raise ValueError(
                "Operator is not allowed."
            )

        return operator_function(
            _evaluate(node.left),
            _evaluate(node.right)
        )

    if isinstance(node, ast.UnaryOp):

        operator_function = (
            _ALLOWED_OPERATORS.get(
                type(node.op)
            )
        )

        if operator_function is None:
            raise ValueError(
                "Unary operator is not allowed."
            )

        return operator_function(
            _evaluate(node.operand)
        )

    raise ValueError(
        "Invalid mathematical expression."
    )


def calculate(expression: str) -> dict:

    if len(expression) > 200:

        raise ValueError(
            "Expression is too long."
        )

    tree = ast.parse(
        expression,
        mode="eval"
    )

    result = _evaluate(
        tree.body
    )

    return {
        "expression": expression,
        "result": result
    }
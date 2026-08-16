# 🚀 Enterprise AI Agent --- AWS-Powered Agentic RAG Application

> A portfolio-grade enterprise AI application demonstrating Generative
> AI, agentic tool calling, RAG, AWS, Docker, security, observability,
> and CI/CD.

## 🎯 Project Motivation

This project was built to demonstrate the complete journey from an AI
prototype to a cloud-deployed application. The goal is to show practical
knowledge of both **AI engineering and AWS/cloud engineering**.

It combines:

-   Python + Streamlit
-   Amazon Bedrock and Amazon Nova Lite
-   Agentic tool calling
-   Retrieval-Augmented Generation (RAG)
-   Amazon Bedrock Knowledge Bases
-   Amazon Bedrock Guardrails
-   Amazon S3
-   Amazon ECS Fargate
-   Amazon ECR
-   AWS IAM
-   AWS Secrets Manager
-   Amazon CloudWatch
-   GitHub Actions + GitHub OIDC
-   Docker
-   Cross-region AWS architecture

## 🧠 What the Application Does

The application provides an AI assistant with two operating modes.

### Knowledge Base OFF

``` text
User
 ↓
Input Guardrail
 ↓
AI Agent
 ↓
Tool Selection
 ├── Weather
 ├── Web Search
 ├── Stock Data
 └── Calculator
 ↓
Output Guardrail
 ↓
Response
```

### Knowledge Base ON

``` text
User
 ↓
Input Guardrail
 ↓
Amazon Bedrock Knowledge Base
 ↓
Relevant Enterprise Document Chunks
 ↓
Amazon Nova Lite
 ↓
Output Guardrail
 ↓
Response
```

When Knowledge Base mode is enabled, the application forces the RAG path
instead of falling through to the normal tool-calling loop.

## 🏗️ Architecture

``` mermaid
flowchart TB
    U[User] --> UI[Streamlit UI]
    UI --> A[Enterprise AI Agent]
    A --> IG[Input Guardrail]
    IG --> M{Knowledge Base ON?}

    M -->|No| T[Agent Tools]
    T --> W[OpenWeather]
    T --> TS[Tavily Search]
    T --> AV[Alpha Vantage]
    T --> C[Calculator]

    M -->|Yes| KB[Bedrock Knowledge Base]
    KB --> S3[S3 Documents]
    KB --> E[Titan Text Embeddings V2]
    KB --> V[Managed Vector Store]
    KB --> CT[Retrieved Context]

    T --> LLM[Amazon Nova Lite]
    CT --> LLM
    LLM --> OG[Output Guardrail]
    OG --> UI

    A --> CW[CloudWatch Logs]
```

## ☁️ AWS Production Architecture

The application runtime is deployed in **AWS Asia Pacific (Sydney),
`ap-southeast-2`**.

The Knowledge Base is maintained in **US East (N. Virginia),
`us-east-1`**.

  Component                     Region
  ----------------------------- ------------------
  ECS Fargate                   `ap-southeast-2`
  ECR                           `ap-southeast-2`
  Secrets Manager               `ap-southeast-2`
  CloudWatch Logs               `ap-southeast-2`
  Application Bedrock runtime   `ap-southeast-2`
  Guardrail                     `ap-southeast-2`
  Knowledge Base                `us-east-1`
  Knowledge Base S3 source      `us-east-1`

This demonstrates a practical **cross-region AWS AI architecture**.

## 📚 RAG Pipeline

``` text
Enterprise Document
 ↓
Amazon S3
 ↓
Amazon Bedrock Knowledge Base
 ↓
Parsing / Chunking
 ↓
Amazon Titan Text Embeddings V2
 ↓
Managed Vector Store
 ↓
Semantic Retrieval
 ↓
Top-K Relevant Chunks
 ↓
RAG Prompt
 ↓
Amazon Nova Lite
 ↓
Grounded Answer
```

Current production configuration:

``` env
AWS_REGION=ap-southeast-2
BEDROCK_KNOWLEDGE_BASE_ID=GGRAPXNGRT
BEDROCK_KNOWLEDGE_BASE_REGION=us-east-1
BEDROCK_MODEL_ID=amazon.nova-lite-v1:0
KNOWLEDGE_BASE_TOP_K=5
```

## 🛡️ Security

### Bedrock Guardrails

Requests pass through an input guardrail and generated responses pass
through an output guardrail:

``` text
User
 ↓
Input Guardrail
 ↓
Agent / RAG
 ↓
Output Guardrail
 ↓
User
```

### IAM

The ECS workload uses:

-   `EnterpriseAIAgentECSTaskRole`
-   `EnterpriseAIAgentECSExecutionRole`

The application uses IAM roles instead of embedding AWS credentials in
source code.

### Secrets Manager

Production API credentials are injected from AWS Secrets Manager:

-   `OPENWEATHER_API_KEY`
-   `TAVILY_API_KEY`
-   `ALPHA_VANTAGE_API_KEY`

The Knowledge Base ID is configuration, not a secret.

### GitHub OIDC

The CI/CD pipeline uses GitHub OIDC rather than long-lived AWS access
keys:

``` text
GitHub Actions
 ↓
OIDC Token
 ↓
AWS IAM OIDC Provider
 ↓
AssumeRoleWithWebIdentity
 ↓
AWS Deployment Permissions
```

This reduces the risk associated with permanent AWS credentials in
GitHub.

## 🐳 Docker + ECS Fargate

The application is containerized with Docker and deployed to Amazon ECS
Fargate.

``` text
Source Code
 ↓
Docker Build
 ↓
Amazon ECR
 ↓
Amazon ECS Fargate
```

Production configuration includes:

``` text
Cluster: EnterpriseAIAgentCluster
Service: EnterpriseAIAgentService
Task Definition: EnterpriseAIAgentTaskDefinition
Launch Type: FARGATE
CPU: 1024
Memory: 2048 MiB
Container Port: 8501
```

The container has an ECS health check against:

``` text
/_stcore/health
```

## 🔄 CI/CD

The deployment pipeline is:

``` text
Developer
 ↓
git push
 ↓
GitHub Actions
 ↓
GitHub OIDC
 ↓
Docker Build
 ↓
ECR Push
 ↓
Render ECS Task Definition
 ↓
ECS Deployment
 ↓
New Fargate Task
 ↓
Health Check
 ↓
Production
```

The ECS task definition is maintained at:

``` text
.aws/task-definition.json
```

Images are tagged using Git commit SHA values for deployment
traceability.

## 📊 Observability

Application logs are sent to Amazon CloudWatch.

Log group:

``` text
/ecs/enterprise-ai-agent
```

Structured logging covers:

-   Agent execution
-   Input guardrail
-   Output guardrail
-   Knowledge Base retrieval
-   Tool selection
-   LLM calls
-   Errors
-   Reliability events

## 🧠 Agent Reliability

The agent includes:

-   Tool execution timeouts
-   Circuit breakers
-   Maximum agent iterations
-   Structured error handling
-   Guardrail checks
-   Controlled tool registry

Configuration:

``` env
MAX_AGENT_ITERATIONS=5
TOOL_TIMEOUT_SECONDS=20
KNOWLEDGE_BASE_TOP_K=5
```

## 🧩 Tools

The agent can work with:

-   OpenWeather API
-   Tavily web search
-   Alpha Vantage
-   Calculator
-   Amazon Bedrock Knowledge Base

The tools are registered centrally so the agent can select capabilities
in normal mode.

## 📁 Project Structure

``` text
Enterprise-AI-Agent/
│
├── .aws/
│   └── task-definition.json
├── .github/
│   └── workflows/
├── backend/
│   ├── agent/
│   │   ├── agent.py
│   │   └── state.py
│   ├── guardrails/
│   │   ├── input.py
│   │   └── output.py
│   ├── llm/
│   │   ├── bedrock.py
│   │   └── prompts.py
│   ├── reliability/
│   │   ├── circuit_breaker.py
│   │   └── timeout.py
│   ├── tools/
│   │   ├── registry.py
│   │   ├── knowledge_base.py
│   │   ├── weather.py
│   │   ├── web_search.py
│   │   ├── stocks.py
│   │   └── calculator.py
│   ├── utils/
│   │   └── logging.py
│   └── main.py
├── frontend/
│   └── streamlit_app.py
├── tests/
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Local Setup

### Prerequisites

-   Python 3.x
-   Docker
-   AWS CLI
-   Git
-   AWS account with required permissions

Create a virtual environment:

``` bash
python -m venv venv
```

Windows:

``` powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

Create `.env` from `.env.example` and configure your local AWS/Bedrock
settings.

### Run

``` bash
streamlit run frontend/streamlit_app.py
```

The application normally runs at:

``` text
http://localhost:8501
```

### Direct RAG Test

``` bash
python -c "from backend.tools.knowledge_base import knowledge_base_tool; print(knowledge_base_tool.search('YOUR QUESTION'))"
```

## 🧪 Validation

The application was tested in three important modes:

1.  **KB OFF** --- normal agent and tools continue to work.
2.  **KB ON + document question** --- the answer is generated from
    retrieved enterprise context.
3.  **KB ON + unrelated question** --- the application does not
    intentionally fall back to unrelated general knowledge.

## 🌐 AWS Infrastructure

The project uses:

-   Amazon VPC
-   Default VPC with 3 Availability Zones
-   Internet Gateway
-   Amazon ECS Fargate
-   Amazon ECR
-   Amazon Bedrock
-   Amazon Bedrock Guardrails
-   Amazon Bedrock Knowledge Bases
-   Amazon S3
-   Amazon Titan Text Embeddings V2
-   Managed vector store
-   AWS IAM
-   AWS Secrets Manager
-   Amazon CloudWatch
-   GitHub Actions
-   GitHub OIDC

## 💰 Cost Awareness

Services such as ECS Fargate, Bedrock inference/retrieval, S3, ECR
storage, and CloudWatch Logs can incur charges. Unused resources should
be removed or stopped in learning environments.

## 🎤 Interview Talking Points

### Why RAG?

> I wanted the model to answer enterprise-specific questions from
> controlled documents rather than relying only on pretrained knowledge.
> I used Amazon Bedrock Knowledge Bases with S3 documents, embeddings,
> semantic retrieval, and a grounded generation step.

### Why ECS Fargate?

> I containerized the application and deployed it with ECS Fargate to
> demonstrate serverless container orchestration without managing EC2
> instances.

### Why ECR?

> ECR provides the private container registry used by the ECS deployment
> pipeline. Images are tagged with commit SHA values so deployments can
> be traced back to source code.

### Why GitHub OIDC?

> I avoided long-lived AWS access keys in GitHub. GitHub Actions uses
> OIDC federation to assume an AWS IAM role for deployment.

### Why Secrets Manager?

> API credentials are runtime secrets, so they are stored in AWS Secrets
> Manager and injected into the ECS container rather than committed to
> source control.

### Why CloudWatch?

> CloudWatch provides centralized production logs for agent execution,
> guardrails, tool calls, RAG retrieval, and failures.

### Why two regions?

> The application runs in Sydney while the Knowledge Base remains in US
> East. The application explicitly separates its runtime region from the
> Knowledge Base region, demonstrating cross-region AWS integration.

### How does the RAG toggle work?

> When disabled, the application follows its normal tool-calling path.
> When enabled, it forces Knowledge Base retrieval, passes the retrieved
> context to Amazon Nova Lite, and returns the grounded response through
> the output guardrail.

## 🚀 Future Improvements

-   [ ] Add clean document citations/source cards
-   [ ] Add authentication and user management
-   [ ] Add conversation persistence
-   [ ] Add metrics dashboards
-   [ ] Add automated integration tests
-   [ ] Add AWS CDK or Terraform
-   [ ] Add Application Load Balancer
-   [ ] Add custom domain and HTTPS
-   [ ] Add blue/green deployment
-   [ ] Add security scanning
-   [ ] Add RAG evaluation metrics
-   [ ] Add document management UI
-   [ ] Add retrieval confidence thresholds
-   [ ] Add streaming responses

## 🏆 Project Summary

This project demonstrates the complete path:

``` text
AI Agent
 ↓
Tool Calling
 ↓
RAG
 ↓
Bedrock Guardrails
 ↓
Docker
 ↓
ECR
 ↓
ECS Fargate
 ↓
IAM + Secrets Manager
 ↓
CloudWatch
 ↓
GitHub Actions
 ↓
GitHub OIDC
 ↓
Production AWS Deployment
```

The main objective was to demonstrate **both AI engineering and cloud
engineering**: building an AI system locally, integrating enterprise
knowledge, securing it, containerizing it, deploying it on AWS,
observing it in production, and automating deployments.

## 👨‍💻 Author

**Lov Kumar**

Repository: https://github.com/lovkumar120169/Enterprise-AI-Agent

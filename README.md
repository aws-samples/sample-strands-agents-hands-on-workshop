# Build a Production AI Agent: Strands Agents Hands-On Workshop

Build a production-ready customer service AI agent from scratch with the [Strands Agents](https://strandsagents.com/latest/?trk=87c4c426-cddf-4799-a299-273337552ad8&sc_channel=el) SDK — the open-source **agent harness SDK** — adding tools, guardrails, memory, multi-agent delegation, evals, and deployment to [Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/?trk=87c4c426-cddf-4799-a299-273337552ad8&sc_channel=el) one module at a time.

![Strands Agents](https://img.shields.io/badge/Strands_Agents-SDK-FF9900?logo=amazonaws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Amazon Bedrock](https://img.shields.io/badge/Amazon_Bedrock-AgentCore-232F3E?logo=amazonaws&logoColor=white)
![License MIT-0](https://img.shields.io/badge/License-MIT--0-green.svg)

> This sample works with Strands Agents and Amazon Bedrock AgentCore. Code in this repository is provided "as is" and is not officially supported by Amazon.

---

## What you'll build

A single customer service agent that grows across 7 modules. Each module is a self-contained notebook (12–15 min) that adds one production capability — starting from a bare agent loop and ending with a deployed agent on AgentCore Runtime. Total time: about 90 minutes.

## What is an agent harness?

An **agent harness** is the system that lets an agent actually run: the orchestration loop that calls the model, decides which tool to invoke, passes results back, manages the context window, and handles failures — plus the infrastructure underneath it (compute, a code sandbox, secure tool connections, persistent storage, memory, identity, and observability).

**Strands Agents is the open-source agent harness SDK** — you don't just write a prompt, you build and control the whole harness (the loop, tools, hooks, memory, guardrails) end-to-end. Amazon Bedrock AgentCore then provides a [managed agent harness](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness.html?trk=87c4c426-cddf-4799-a299-273337552ad8&sc_channel=el) that runs it in production — and the [AgentCore harness is powered by Strands Agents](https://strandsagents.com/?trk=87c4c426-cddf-4799-a299-273337552ad8&sc_channel=el), so the harness you build is the harness that ships. This workshop builds it layer by layer:

| Stage | What you do | With |
|-------|------------|------|
| Build the harness | Assemble the loop, tools, hooks, skills, memory, multi-agent, and evals — controlling each layer | Strands Agents (Modules 1–6) |
| Run the harness | Operate the same harness in production — managed compute, memory, identity, observability | Amazon Bedrock AgentCore Runtime (Module 7) |

Because the harness is config-driven, trying a different model or adding a tool is a config change, not a code rewrite.

## Modules

| # | Module | Time | What you'll build |
|---|--------|------|-------------------|
| 1 | [Agent Loop + Tools](./samples/01-agent-loop-tools/) | 12 min | Customer service agent with lookup, orders, and refund tools |
| 2 | [Hooks](./samples/02-hooks/) | 10 min | Rate limiter that caps runaway tool calls with deterministic code |
| 3 | [Skills + Steering](./samples/03-skills-steering/) | 15 min | Workflow skills, refund enforcement, and a tone guardrail |
| 4 | [Session Managers](./samples/04-session-managers/) | 10 min | Persistent memory that survives restarts |
| 5 | [Multi-Agent](./samples/05-multi-agent/) | 15 min | Delegation to a tech support specialist agent |
| 6 | [Evals](./samples/06-evals/) | 13 min | Automated quality testing with LLM-as-judge |
| 7 | [Deploy](./samples/07-deploy/) | 15 min | Deployment to Amazon Bedrock AgentCore Runtime |

Shared mock tools used across modules live in [`samples/shared/`](./samples/shared/).

---

## How do I get started?

The fastest path is to open Module 1 and run the notebook cells top to bottom. Each module's README explains the concept and links to the next.

```bash
# Clone the repo
git clone https://github.com/aws-samples/sample-strands-agents-hands-on-workshop.git
cd sample-strands-agents-hands-on-workshop
```

Then open [`samples/01-agent-loop-tools/`](./samples/01-agent-loop-tools/) in **VS Code** or **JupyterLab** and run the notebook.

## How do I set up the environment?

This workshop runs in a hosted VS Code environment with dependencies pre-installed. To run locally:

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies (or use each module's requirements.txt)
pip install strands-agents strands-agents-evals bedrock-agentcore

# Configure AWS credentials (Strands uses Amazon Bedrock by default)
aws configure
```

Each module also ships its own `requirements.txt`, so you can install only what that module needs.

## What are the prerequisites?

| Requirement | Detail |
|-------------|--------|
| Python | 3.10 or higher |
| AWS credentials | Amazon Bedrock model access for Claude Sonnet 4 |
| Extra permissions (Module 7) | AWS Lambda, AgentCore Gateway, AgentCore Memory |

---

## How does the agent loop work?

The agent loop cycles between the LLM and your tools until the model has enough information to answer: `User → LLM → Tool Call → Tool Result → LLM → Response`. Tools are plain Python functions decorated with `@tool`, and the LLM reads each docstring to decide when to call them — no manual routing required.

```python
from strands import Agent, tool

@tool
def lookup_customer(customer_id: str) -> str:
    """Look up a customer by their ID."""
    ...

agent = Agent(tools=[lookup_customer], system_prompt=SYSTEM_PROMPT)
agent("I'm C-1001. What are my recent orders?")
```

See [Module 1](./samples/01-agent-loop-tools/) for the full walkthrough and an inspection of the loop in action.

---

## Frequently asked questions

**Do I need to complete the modules in order?**
Yes. Each module builds on the previous one — the same customer service agent gains a new capability in every module.

**Which Claude model does this use?**
The modules default to Claude Sonnet 4 via Amazon Bedrock. You need Bedrock model access enabled in your AWS account.

**What is the difference between an agent framework and an agent harness?**
A framework gives you the orchestration loop (model calls, tool selection, context). A harness is the full system that lets the agent run: the loop *plus* compute, a code sandbox, tool connections, memory, identity, and observability. Strands Agents is positioned as an agent harness SDK; Amazon Bedrock AgentCore provides a managed harness so you skip building that infrastructure from scratch.

**Can I use a framework other than Strands Agents?**
The patterns shown here — tool use, hooks, session memory, multi-agent handoff, and LLM-as-judge evals — are framework-agnostic and map to LangGraph, AutoGen, and CrewAI. AgentCore is also framework-agnostic: it runs agents from any framework, not only Strands. This workshop implements the patterns with the Strands Agents SDK.

**How long does the full workshop take?**
About 90 minutes for all 7 modules. Each module is self-contained and takes 10–15 minutes.

**Do I need AWS resources to run the early modules?**
You need Amazon Bedrock access from Module 1. Additional services (AWS Lambda, AgentCore Gateway, AgentCore Memory) are only required for the deployment module.

---

## Resources

- [Strands Agents Documentation](https://strandsagents.com/latest/?trk=87c4c426-cddf-4799-a299-273337552ad8&sc_channel=el)
- [Strands Agents SDK on GitHub](https://github.com/strands-agents/sdk-python)
- [Amazon Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/?trk=87c4c426-cddf-4799-a299-273337552ad8&sc_channel=el)
- [AgentCore harness (managed agent harness)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness.html?trk=87c4c426-cddf-4799-a299-273337552ad8&sc_channel=el)
- [Full Video Course](https://github.com/morganwillisaws/strands-course) — Deep dives on every topic covered here

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](http://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file for details.

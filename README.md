# Strands Agents Hands-On Workshop

Build a production-ready AI agent from scratch using the Strands Agents SDK.

## Build Your First Agent Harness (90 min)

Build a customer service agent step by step, adding capabilities each module.

| # | Module | Time | What You'll Build |
|---|---|---|---|
| 1 | Agent Loop + Tools | 12 min | Customer service agent with lookup, orders, and refund tools |
| 2 | Hooks | 10 min | Rate limiter to prevent runaway tool calls |
| 3 | Skills + Steering | 15 min | Workflow skills + refund enforcement + tone guardrail |
| 4 | Session Managers | 10 min | Persistent memory across restarts |
| 5 | Multi-Agent | 15 min | Delegate to a tech support specialist |
| 6 | Evals | 13 min | Automated quality testing with LLM-as-judge |
| 7 | Deploy | 15 min | Deploy to AgentCore Runtime |

**Location:** `samples/`

## Environment Setup

This workshop runs in a hosted VS Code environment with dependencies pre-installed.

If running locally:

```bash
# Clone the repo
git clone https://github.com/aws-samples/sample-strands-agents-hands-on-workshop.git
cd sample-strands-agents-hands-on-workshop

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies (or use each module's requirements.txt)
pip install strands-agents strands-agents-evals bedrock-agentcore

# Configure AWS credentials (Strands uses Bedrock by default)
aws configure
```

## Prerequisites

- Python 3.10+
- AWS credentials with Bedrock model access (Claude Sonnet 4)
- For Workshop 2: Additional permissions for Lambda, AgentCore Gateway, AgentCore Memory

## Resources

- [Strands Agents Documentation](https://strandsagents.com/?trk=87c4c426-cddf-4799-a299-273337552ad8&sc_channel=el)
- [Strands GitHub](https://github.com/strands-agents/sdk-python)
- [Full Video Course](https://github.com/morganwillisaws/strands-course) — Deep dives on every topic covered here
- [AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/?trk=87c4c426-cddf-4799-a299-273337552ad8&sc_channel=el)

---

## Contributing

Contributions are welcome! See [CONTRIBUTING](CONTRIBUTING.md) for more information.

---

## Security

If you discover a potential security issue in this project, notify AWS/Amazon Security via the [vulnerability reporting page](http://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public GitHub issue.

---

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file for details.

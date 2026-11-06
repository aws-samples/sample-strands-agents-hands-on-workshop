"""Interactive multi-turn chat for Module 4: Session Managers.

The notebook runs the agent one prompt at a time (each cell is one turn). This
script wraps the same agent - backed by SnapshotSessionManager - in a loop so
you can hold a real multi-turn conversation in the terminal.

Because the session is persisted to disk, this is also the persistence demo:
quit the script, run it again with the same --session-id, and the agent
remembers the earlier conversation.

From the cloned repo root:

    cd samples/04-session-managers
    pip install -r requirements.txt
    python chat.py                       # uses the default session id
    python chat.py --session-id alice    # resume/keep a named session

Type 'quit', 'exit', or press Ctrl+C to stop.
"""

import argparse

from strands import Agent, AgentSkills
from strands.models import BedrockModel
from strands.session import SnapshotSessionManager
from strands.storage import LocalFileStorage

# AWS-sponsored events / AWS credits: credits only cover Amazon Nova models, not Claude.
# To switch, pass model=BedrockModel(model_id="...") to Agent(...).
# Nova model IDs: https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards-amazon.html
#   amazon.nova-micro-v1:0  — fastest, text-only, lowest cost
#   amazon.nova-lite-v1:0   — low-cost, multimodal (text, image, video)
#   amazon.nova-pro-v1:0    — balanced accuracy/speed, multimodal (recommended)
#
# Run locally without AWS credentials using Ollama (https://ollama.com/download):
#   1. Install Ollama and run: ollama pull llama3.1
#   2. pip install strands-agents[ollama]
#   3. Use OllamaModel: from strands.models import OllamaModel
#      model = OllamaModel(host="http://localhost:11434", model_id="llama3.1")
#      agent = Agent(model=model, tools=[...], session_manager=..., system_prompt=...)
#   Other models with tool support: llama3.2, qwen2.5, qwen3, mistral
from customer_service_tools import lookup_customer, get_order_history, process_refund

SYSTEM_PROMPT = """You are a customer service agent for an online electronics store.
Be helpful, professional, and concise.

If there are previous messages in the conversation history, use that context
to continue helping the customer without asking them to repeat information."""


def main():
    parser = argparse.ArgumentParser(description="Multi-turn chat with a persistent agent.")
    parser.add_argument(
        "--session-id",
        default="customer-session-001",
        help="Session id to persist/resume (default: customer-session-001).",
    )
    args = parser.parse_args()

    # SnapshotSessionManager persists the whole agent as one atomic blob via the
    # unified Storage backend. Use LocalFileStorage for dev; swap it for
    # S3Storage (strands.storage.S3Storage) in production without other changes.
    # Reusing the same session_id across runs restores the prior conversation.
    session_manager = SnapshotSessionManager(
        session_id=args.session_id,
        storage=LocalFileStorage("./sessions"),
    )

    agent = Agent(
        tools=[lookup_customer, get_order_history, process_refund],
        plugins=[AgentSkills(skills=["./skills"])],
        system_prompt=SYSTEM_PROMPT,
        # context_manager="auto" offloads large tool results, compresses old
        # messages into summaries, and fires proactive compression at 85% usage.
        context_manager="auto",
        session_manager=session_manager,
    )

    restored = len(agent.messages)
    print(f"Customer service agent (persistent session: {args.session_id}) - type 'quit' to exit.")
    if restored:
        print(f"Restored {restored} message(s) from a previous session.")
    print("Try: \"Hi, I'm customer C-1001. Can you look up my account?\"")
    print("Then quit and run again - it remembers who you are.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! Your conversation is saved.")
            break

        if user_input.lower() in {"quit", "exit", "q"}:
            print("Goodbye! Your conversation is saved.")
            break
        if not user_input:
            continue

        print("\nAgent: ", end="")
        agent(user_input)
        print()


if __name__ == "__main__":
    main()

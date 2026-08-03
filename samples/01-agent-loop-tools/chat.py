"""Interactive multi-turn chat for Module 1: Agent Loop + Tools.

The notebook runs the agent one prompt at a time (each cell is one turn). This
script wraps the same agent in a loop so you can hold a real multi-turn
conversation in the terminal - the agent keeps its context across turns.

From the cloned repo root:

    cd samples/01-agent-loop-tools
    pip install -r requirements.txt
    python chat.py

Type 'quit', 'exit', or press Ctrl+C to stop.
"""

from strands import Agent
from strands.models import BedrockModel
from customer_service_tools import lookup_customer, get_order_history, process_refund

# AWS-sponsored events / AWS credits: credits only cover Amazon Nova models, not Claude.
# To switch, pass model=BedrockModel(model_id="...") to Agent(...).
# Nova model IDs: https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards-amazon.html
#   amazon.nova-micro-v1:0  — fastest, text-only, lowest cost
#   amazon.nova-lite-v1:0   — low-cost, multimodal (text, image, video)
#   amazon.nova-pro-v1:0    — balanced accuracy/speed, multimodal (recommended)

SYSTEM_PROMPT = """You are a customer service agent for an online electronics store.
Be helpful, professional, and concise. Use the available tools to look up customer
information and process requests.

Important guidelines:
- Always verify the customer using lookup_customer before taking action.
- Use tool data to answer questions - don't ask the customer for info you already have.
- Be warm but efficient."""


def main():
    # One agent instance reused across turns - it keeps conversation history in
    # agent.messages, which is what makes the conversation multi-turn.
    agent = Agent(
        tools=[lookup_customer, get_order_history, process_refund],
        system_prompt=SYSTEM_PROMPT,
    )

    print("Customer service agent - type 'quit' to exit.")
    print("Try: \"Hi, I'm customer C-1001. What are my recent orders?\"\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break
        if not user_input:
            continue

        # The agent prints its own streamed response via the default callback handler.
        print("\nAgent: ", end="")
        agent(user_input)
        print()


if __name__ == "__main__":
    main()

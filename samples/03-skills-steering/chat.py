"""Interactive multi-turn chat for Module 3: Skills + Steering.

The notebook runs the agent one prompt at a time (each cell is one turn). This
script wraps the same agent - with the workflow skills and both steering
handlers from the module - in a loop so you can hold a real multi-turn
conversation in the terminal.

From the cloned repo root:

    cd samples/03-skills-steering
    pip install -r requirements.txt
    python chat.py

Type 'quit', 'exit', or press Ctrl+C to stop.
"""

from strands import Agent, AgentSkills
from strands.models import BedrockModel
from customer_service_tools import lookup_customer, get_order_history, process_refund

# AWS-sponsored events / AWS credits: credits only cover Amazon Nova models, not Claude.
# To switch, pass model=BedrockModel(model_id="...") to Agent(...).
# Nova model IDs: https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards-amazon.html
#   amazon.nova-micro-v1:0  — fastest, text-only, lowest cost
#   amazon.nova-lite-v1:0   — low-cost, multimodal (text, image, video)
#   amazon.nova-pro-v1:0    — balanced accuracy/speed, multimodal (recommended)
from steering_handlers import RefundWorkflowHandler, tone_handler

SYSTEM_PROMPT = """You are a customer service agent for an online electronics store.
Be helpful, professional, and concise. Use the available tools to look up customer
information and process requests. When a customer needs help, activate the appropriate
skill for step-by-step guidance.

Important guidelines:
- Always ask for the customer ID first if you don't have it.
- Use the data returned by tools to answer questions.
- Be warm but efficient."""


def main():
    # One agent instance reused across turns keeps conversation history in
    # agent.messages, which is what makes the conversation multi-turn. The skills
    # and steering handlers apply on every turn.
    agent = Agent(
        tools=[lookup_customer, get_order_history, process_refund],
        plugins=[
            AgentSkills(skills=["./skills"]),
            RefundWorkflowHandler(),
            tone_handler,
        ],
        system_prompt=SYSTEM_PROMPT,
    )

    print("Customer service agent (skills + steering) - type 'quit' to exit.")
    print("Try: \"I'm customer C-1001. I want a refund for order ORD-5521.\"\n")

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

        print("\nAgent: ", end="")
        agent(user_input)
        print()


if __name__ == "__main__":
    main()

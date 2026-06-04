import json
import logging
import os
from strands import Agent
from strands.agent.conversation_manager import SlidingWindowConversationManager
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from customer_service_tools import lookup_customer, get_order_history, process_refund
from steering_handlers import RefundWorkflowHandler, tone_handler

logger = logging.getLogger(__name__)

app = BedrockAgentCoreApp()

SYSTEM_PROMPT = """You are a customer service agent for an online electronics store.
Be helpful, professional, and concise. Use the available tools to look up customer
information and process requests.

Important guidelines:
- Always ask for the customer ID first if you don't have it.
- Use tool data to answer questions — don't ask for info you already have.
- Be warm but efficient."""

_agent = None

def get_agent():
    global _agent
    if _agent is None:
        _agent = Agent(
            tools=[lookup_customer, get_order_history, process_refund],
            plugins=[RefundWorkflowHandler(), tone_handler],
            system_prompt=SYSTEM_PROMPT,
            conversation_manager=SlidingWindowConversationManager(window_size=20),
        )
    return _agent


@app.entrypoint
def invoke(payload, context):
    raw_prompt = payload.get("prompt")
    try:
        parsed = json.loads(raw_prompt)
        prompt = parsed.get("prompt", raw_prompt)
    except (TypeError, json.JSONDecodeError):
        prompt = raw_prompt

    if not prompt:
        raise ValueError("Missing required field: prompt")

    agent = get_agent()
    response = agent(prompt)
    return {"response": str(response)}


if __name__ == "__main__":
    app.run()

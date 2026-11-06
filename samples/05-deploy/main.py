import json
import logging
import os
from strands import Agent
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
- Use tool data to answer questions, don't ask for info you already have.
- Be warm but efficient."""

_agent = None
_pending_interrupts = []

def get_agent():
    global _agent
    if _agent is None:
        _agent = Agent(
            tools=[lookup_customer, get_order_history, process_refund],
            plugins=[RefundWorkflowHandler(), tone_handler],
            system_prompt=SYSTEM_PROMPT,
            context_manager="auto",
        )
    return _agent


def interrupt_response(interrupts):
    """Describe the tool calls waiting for human approval so the caller can answer them."""
    return {
        "status": "interrupted",
        "interrupts": [
            {"interruptId": interrupt.id, "name": interrupt.name, "reason": interrupt.reason}
            for interrupt in interrupts
        ],
    }


@app.entrypoint
def invoke(payload, context):
    global _pending_interrupts
    agent = get_agent()

    # Resume a paused invocation: {"interrupt_responses": [{"interruptId": "...", "response": true}]}
    interrupt_responses = payload.get("interrupt_responses")
    if interrupt_responses:
        result = agent([{"interruptResponse": response} for response in interrupt_responses])
    else:
        raw_prompt = payload.get("prompt")
        try:
            parsed = json.loads(raw_prompt)
            prompt = parsed.get("prompt", raw_prompt)
        except (TypeError, json.JSONDecodeError):
            prompt = raw_prompt

        if not prompt:
            raise ValueError("Missing required field: prompt")

        # The agent can't take a new prompt until the pending interrupts are answered
        if _pending_interrupts:
            return interrupt_response(_pending_interrupts)

        result = agent(prompt)

    # A steering handler paused a tool call for human approval
    if result.stop_reason == "interrupt":
        _pending_interrupts = list(result.interrupts)
        return interrupt_response(_pending_interrupts)

    _pending_interrupts = []
    return str(result).strip()


if __name__ == "__main__":
    app.run()

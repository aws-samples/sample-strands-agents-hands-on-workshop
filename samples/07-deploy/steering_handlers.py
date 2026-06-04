"""
Steering handlers for the customer service agent deployment.
"""

import re
from strands.vended_plugins.steering import (
    SteeringHandler, LLMSteeringHandler,
    Proceed, Guide, ToolSteeringAction,
    LedgerProvider,
)


class RefundWorkflowHandler(SteeringHandler):
    """Deterministic handler: enforce refund workflow ordering.

    Rules:
    1. Must look up the customer before processing a refund
    2. Must check order history before processing a refund
    """

    name = "refund-workflow"

    def __init__(self):
        super().__init__(context_providers=[LedgerProvider()])

    async def steer_before_tool(self, *, agent, tool_use, **kwargs) -> ToolSteeringAction:
        if tool_use.get("name") != "process_refund":
            return Proceed(reason="Not a refund operation")

        ledger = self.steering_context.data.get("ledger", {})
        tool_calls = ledger.get("tool_calls", [])

        customer_verified = any(
            c["tool_name"] == "lookup_customer" and c["status"] == "success"
            for c in tool_calls
        )
        if not customer_verified:
            return Guide(
                reason="You must look up the customer with lookup_customer "
                "before processing a refund."
            )

        order_checked = any(
            c["tool_name"] == "get_order_history" and c["status"] == "success"
            for c in tool_calls
        )
        if not order_checked:
            return Guide(
                reason="You must check the order history with get_order_history "
                "before processing a refund."
            )

        return Proceed(reason="Refund workflow validated")


class ToneGuardrailHandler(LLMSteeringHandler):
    """LLM-based handler: evaluates response tone and professionalism."""

    name = "tone-guardrail"

    def __init__(self):
        super().__init__(
            system_prompt="""You are evaluating a customer service agent's responses.
Ensure the agent follows these communication guidelines:

- Don't overpromise or guarantee specific timelines beyond what the system confirms
- Don't blame the customer, other departments, or third parties
- Acknowledge the customer's frustration before jumping to solutions
- Keep responses concise and actionable
- Never share internal system details or technical jargon with the customer

If the agent violates any of these, provide specific guidance on what to fix."""
        )

    async def steer_after_model(self, **kwargs):
        return await super().steer_after_model(**kwargs)


tone_handler = ToneGuardrailHandler()

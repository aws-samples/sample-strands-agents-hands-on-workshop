"""Interactive multi-turn chat for Module 6: Multi-Agent (Optional).

The notebook runs the orchestrator one prompt at a time (each cell is one turn).
This script wraps the same orchestrator - which delegates technical issues to a
tech support specialist via the agents-as-tools pattern - in a loop so you can
hold a real multi-turn conversation in the terminal.

From the cloned repo root:

    cd samples/06-multi-agent
    pip install -r requirements.txt
    python chat.py

Type 'quit', 'exit', or press Ctrl+C to stop.
"""

from strands import Agent, tool
from customer_service_tools import lookup_customer, get_order_history, process_refund


# --- Tech support tools (specialist-only) ---

@tool
def check_device_compatibility(device: str, issue: str) -> str:
    """Check if a device has known compatibility issues.

    Args:
        device: The device name or model
        issue: Description of the issue
    """
    known_issues = {
        "Wireless Headphones": "Known Bluetooth 5.0 pairing issue with older devices. Fix: Reset headphones (hold power 10s), then re-pair.",
        "USB-C Hub": "Some laptops require USB-C alt mode. Check laptop specs for DisplayPort over USB-C support.",
        "Mechanical Keyboard": "Firmware v2.1 has a key ghosting bug. Update to v2.3 via manufacturer website.",
    }
    for device_name, fix in known_issues.items():
        if device_name.lower() in device.lower():
            return f"Known issue found for {device_name}: {fix}"
    return f"No known issues found for '{device}'. Recommend standard troubleshooting: restart device, check connections, update drivers."


@tool
def run_diagnostic(device: str) -> str:
    """Run a remote diagnostic check on a device.

    Args:
        device: The device name or model to diagnose
    """
    return (
        f"Diagnostic results for {device}:\n"
        f"- Firmware: v2.1 (update available: v2.3)\n"
        f"- Connection: Stable\n"
        f"- Battery: 85%\n"
        f"- Last sync: 2 hours ago\n"
        f"Recommendation: Update firmware to resolve known issues."
    )


@tool
def tech_support_specialist(issue_description: str) -> str:
    """Escalate a technical issue to the tech support specialist agent.
    Use this when a customer has a device problem, connectivity issue,
    or needs technical troubleshooting beyond basic order/account help.

    Args:
        issue_description: Detailed description of the technical issue including device name and symptoms
    """
    specialist = Agent(
        tools=[check_device_compatibility, run_diagnostic],
        system_prompt="""You are a tech support specialist for an electronics store.
You diagnose device issues, check compatibility, and provide step-by-step fixes.
Be technical but clear. Always provide actionable next steps.""",
        callback_handler=None,  # Silent - don't stream the specialist's output to the user
    )
    print(f"\n[DELEGATION] 🔧 Tech support specialist activated")
    response = specialist(issue_description)
    print(f"[DELEGATION] ✅ Specialist responded")
    return str(response)


SYSTEM_PROMPT = """You are a customer service agent for an online electronics store.
Be helpful, professional, and concise.

You handle:
- Account lookups and order status
- Refund processing
- Basic questions

For TECHNICAL issues (device problems, connectivity, firmware, troubleshooting),
delegate to the tech_support_specialist tool. Provide it with the device name
and a clear description of the issue.

After getting the specialist's response, relay the solution to the customer
in a friendly, non-technical way."""


def main():
    # One orchestrator reused across turns keeps conversation history in
    # agent.messages, which is what makes the conversation multi-turn.
    orchestrator = Agent(
        tools=[lookup_customer, get_order_history, process_refund, tech_support_specialist],
        system_prompt=SYSTEM_PROMPT,
    )

    print("Customer service orchestrator (delegates to a specialist) - type 'quit' to exit.")
    print("Try: \"I'm C-1001. My wireless headphones won't pair with my phone.\"\n")

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
        orchestrator(user_input)
        print()


if __name__ == "__main__":
    main()

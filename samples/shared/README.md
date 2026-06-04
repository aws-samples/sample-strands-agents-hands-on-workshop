# Shared Tools

Mock customer service tools used across the Workshop 1 modules. They simulate a backend so you can focus on agent patterns instead of real infrastructure.

## What's here

| Tool | What it does |
|------|--------------|
| `lookup_customer(customer_id)` | Returns name, email, phone, and account status |
| `get_order_history(customer_id)` | Returns orders with status, dates, and tracking |
| `process_refund(order_id, amount)` | Returns a refund confirmation message |

Data is hard-coded in `customer_service_tools.py` (customers `C-1001`, `C-1002`). Each module keeps its own copy of this file so it runs independently.

## Usage

```python
from customer_service_tools import lookup_customer, get_order_history, process_refund

agent = Agent(tools=[lookup_customer, get_order_history, process_refund])
```

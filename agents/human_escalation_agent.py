from datetime import datetime


def human_escalation_agent(user_query, reason="Unable to confidently answer"):
    ticket_id = "PF-" + datetime.now().strftime("%Y%m%d%H%M%S")

    response = f"""
## Human Escalation Required

Your request may require human review.

## Escalation Reason
{reason}

## Your Query
{user_query}

## Ticket ID
{ticket_id}

## Next Step
A human career advisor should review this case manually.

## Suggested Human Review Areas
- Resume suitability
- Career transition risk
- Sensitive personal information
- Complex or unclear user request
"""

    return response


if __name__ == "__main__":
    sample_query = "I am very confused and need someone to personally review my career situation."

    result = human_escalation_agent(
        sample_query,
        reason="User requested personal human assistance"
    )

    print("\nCareer&Skills AI - Human Escalation Agent Test")
    print("-" * 60)
    print(result)
import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

api_key = os.getenv("HINDSIGHT_API_KEY")

if not api_key:
    raise ValueError("HINDSIGHT_API_KEY is missing from .env")

client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=api_key
)

BANK_ID = "incident-response-agent"

try:
    # Create memory bank
    client.create_bank(
        bank_id=BANK_ID,
        name="Incident Response Agent"
    )

    print("✅ Hindsight memory bank ready!")

    # Store a previous security incident
    client.retain(
        bank_id=BANK_ID,
        content="""
        Incident: Production database connectivity failure.
        Severity: High.
        Root cause: Firewall misconfiguration.
        Resolution: Updated firewall rules and restored database access.
        Outcome: Incident resolved successfully.
        """
    )

    print("✅ Incident memory stored!")

    # Recall similar incident
    result = client.recall(
        bank_id=BANK_ID,
        query="Find previous incidents related to database connectivity problems."
    )

    print("\n🔎 Recalled memories:")

    if result.results:
        for memory in result.results:
            print("-", memory.text)
    else:
        print("No memories found.")

finally:
    client.close()
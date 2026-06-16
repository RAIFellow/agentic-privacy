import time
import random


class NegotiationAgent:
    def __init__(self, name, role, min_acceptable, max_acceptable, preferred):
        self.name = name
        self.role = role
        self.min_retention = min_acceptable  # in days
        self.max_retention = max_acceptable  # in days
        self.current_proposal = preferred
        self.negotiation_history = []

    def propose(self, counter_proposal=None):
        if counter_proposal is None:
            return self.current_proposal

        # Concession logic: Move slowly toward the counter-proposal if within bounds
        if self.role == "Provider":
            # Provider wants less time, so they slowly increase their offer
            if counter_proposal > self.current_proposal:
                step = random.randint(5, 15)
                self.current_proposal = min(self.current_proposal + step, self.max_retention)
        else:
            # Consumer wants more time, so they slowly decrease their demand
            if counter_proposal < self.current_proposal:
                step = random.randint(5, 15)
                self.current_proposal = max(self.current_proposal - step, self.min_retention)

        return self.current_proposal

    def evaluate(self, offered_terms):
        """Evaluates if the offered terms are acceptable."""
        if self.min_retention <= offered_terms <= self.max_retention:
            return "ACCEPT"
        return "COUNTER"


def run_negotiation():
    # Initialize Agents
    # Provider prefers 30 days, can stretch to 90 max.
    provider = NegotiationAgent(
        name="PrivacyGuard_Agent",
        role="Provider",
        min_acceptable=14,
        max_acceptable=90,
        preferred=30
    )

    # Consumer prefers 180 days, can squeeze down to 60 min.
    consumer = NegotiationAgent(
        name="AnalyticsMax_Agent",
        role="Consumer",
        min_acceptable=60,
        max_acceptable=365,
        preferred=180
    )

    print("=== Starting Autonomous Data Retention Negotiation ===")
    print(f"{provider.name} (Provider) Preferred: {provider.current_proposal} days")
    print(f"{consumer.name} (Consumer) Preferred: {consumer.current_proposal} days\n")
    print("-" * 60)

    turn = "Consumer"
    current_offer = consumer.propose()
    print(f"Round 1 | {consumer.name} opens the negotiation demanding: {current_offer} days.")

    max_rounds = 10
    for round_num in range(2, max_rounds + 1):
        time.sleep(0.5)  # Simulate processing time

        if turn == "Consumer":
            # Provider evaluates Consumer's offer
            decision = provider.evaluate(current_offer)
            if decision == "ACCEPT":
                print(f"\n>> SUCCESS: {provider.name} accepted the offer of {current_offer} days!")
                break
            else:
                current_offer = provider.propose(counter_proposal=current_offer)
                print(f"Round {round_num} | {provider.name} rejects and counters with: {current_offer} days.")
                turn = "Provider"

        else:
            # Consumer evaluates Provider's offer
            decision = consumer.evaluate(current_offer)
            if decision == "ACCEPT":
                print(f"\n>> SUCCESS: {consumer.name} accepted the offer of {current_offer} days!")
                break
            else:
                current_offer = consumer.propose(counter_proposal=current_offer)
                print(f"Round {round_num} | {consumer.name} rejects and counters with: {current_offer} days.")
                turn = "Consumer"
    else:
        print("\n>> FAILURE: Agents failed to reach an agreement within the round limit.")


if __name__ == "__main__":
    run_negotiation()
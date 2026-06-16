
import re

class PrivacyAgent:
    def __init__(self, user_name, raw_preferences):
        self.user_name = user_name
        self.user_data = {
            "date_of_birth": "1995-08-24",
            "email": "user@example.com",
            "phone": "+1-555-312-0199"
        }
        # Parse the raw preference string into structured rules
        self.rules = self._parse_preferences(raw_preferences)

    def _parse_preferences(self, preference_text):
        """
        Simulates an Agent's NLP capability to extract rules from text.
        Converts 'only share X with Y' into a structured dictionary.
        """
        rules = {}
        text_lower = preference_text.lower()

        # Look for date of birth pattern
        if "date of birth" in text_lower or "dob" in text_lower:
            if "only share" in text_lower and ".gov" in text_lower:
                rules["date_of_birth"] = {
                    "restriction": "strict_domain_match",
                    "allowed_suffix": ".gov"
                }

        # You could expand this NLP parser to extract other rules
        return rules

    def process_data_request(self, requesting_domain, requested_field):
        """
        The core agentic logic: Evaluates incoming requests against user rules.
        """
        print(f"\n[Agent Notification]: {requesting_domain} is requesting your '{requested_field}'.")

        # Check if the requested data exists
        if requested_field not in self.user_data:
            return f"❌ Request Denied: Field '{requested_field}' does not exist."

        # Check if there is a specific rule for this data field
        if requested_field in self.rules:
            rule = self.rules[requested_field]

            # Evaluate "strict_domain_match" rule (e.g., must end in .gov)
            if rule["restriction"] == "strict_domain_match":
                allowed_suffix = rule["allowed_suffix"]

                if requesting_domain.endswith(allowed_suffix):
                    return f"✅ Request Approved: '{requesting_domain}' matches your rule ({allowed_suffix}). Sending data: {self.user_data[requested_field]}"
                else:
                    return (f"❌ Request Denied: Your settings state you only share {requested_field} "
                            f"with {allowed_suffix} sites. '{requesting_domain}' was blocked.")

        # Default behavior if no rules are set
        return f"⚠️ No rule found. Prompting user for permission to share with {requesting_domain}."


# ==========================================
# SIMULATION
# ==========================================
if __name__ == "__main__":
    # 1. Initialize the agent with the user's natural language preference
    user_pref = "Only share my date of birth with .gov sites"

    print("=== Initializing Agentic Privacy Hub ===")
    my_privacy_agent = PrivacyAgent(user_name="Alex", raw_preferences=user_pref)
    print(f"User Preference loaded: \"{user_pref}\"")
    print(f"Parsed Rule: {my_privacy_agent.rules}")
    print("-" * 60)

    # 2. Simulate Facebook.com requesting the Date of Birth
    fb_response = my_privacy_agent.process_data_request(
        requesting_domain="facebook.com",
        requested_field="date_of_birth"
    )
    print(f"Decision: {fb_response}")
    print("-" * 60)

    # 3. Simulate a Government site requesting the Date of Birth to show contrast
    gov_response = my_privacy_agent.process_data_request(
        requesting_domain="irs.gov",
        requested_field="date_of_birth"
    )
    print(f"Decision: {gov_response}")
    print("-" * 60)
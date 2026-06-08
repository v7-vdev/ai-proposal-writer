import re

def validate_proposal_accuracy(proposal_text, target_budget, client_name, project_name):
    """
    Basic validation to check if the proposal follows constraints.
    """
    errors = []
    
    # 1. Check for Budget
    if target_budget not in proposal_text:
        errors.append(f"Target budget '{target_budget}' not found in the proposal.")
    
    # 2. Check for placeholders
    placeholders = re.findall(r'\[.*?\]', proposal_text)
    if placeholders:
        # Filter out common markdown or intentional brackets if any, but usually they are placeholders
        errors.append(f"Found potential placeholders: {placeholders}")
        
    # 3. Check for natural integration
    if client_name.lower() not in proposal_text.lower():
        errors.append(f"Client name '{client_name}' not mentioned in the proposal.")
    if project_name.lower() not in proposal_text.lower():
        errors.append(f"Project name '{project_name}' not mentioned in the proposal.")

    # 4. Pricing Sum Validation (Heuristic)
    # This tries to find currency amounts and see if any subset sums to the budget
    # In a real test, we might use an LLM to verify another LLM's math, 
    # but here we'll do a simple regex check for the 'Pricing Section'
    pricing_section = re.search(r'Pricing Section(.*?)(?=\n#|$)', proposal_text, re.S)
    if pricing_section:
        content = pricing_section.group(1)
        # Find all numbers that look like prices (e.g., $1,200 or 1200)
        amounts = re.findall(r'\$?\d+(?:,\d+)?(?:\.\d+)?', content)
        # Clean amounts
        clean_amounts = []
        for a in amounts:
            num = re.sub(r'[$,]', '', a)
            try:
                clean_amounts.append(float(num))
            except ValueError:
                continue
        
        target_val = float(re.sub(r'[$,]', '', target_budget))
        
        # Check if the sum of all components (excluding the total itself if repeated) equals target
        # This is a bit complex for a heuristic, so we'll just check if the total is mentioned in pricing
        if target_val not in clean_amounts:
             errors.append(f"Target budget value {target_val} not found in Pricing Section amounts.")
    else:
        errors.append("Pricing Section not found.")

    return errors

if __name__ == "__main__":
    # Example test
    sample_proposal = """
# Proposal for TechNova Solutions
## Executive Summary
We are excited to work on the E-Commerce Platform Overhaul project for TechNova Solutions...
## Pricing Section
- Design: $5,000
- Development: $7,000
- Integration: $500
- **Total: $12,500**
    """
    results = validate_proposal_accuracy(sample_proposal, "$12,500", "TechNova Solutions", "E-Commerce Platform Overhaul")
    if not results:
        print("Test Passed: Proposal looks accurate.")
    else:
        print("Test Failed Errors:", results)

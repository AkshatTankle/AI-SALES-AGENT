from AI_SALES import SalesAgent # This correctly imports from your file

def main():
    """
    Main function to run the AI Sales Agent.
    """
    try:
        agent = SalesAgent()
    except ValueError as e:
        print(e)
        return

    # 1. Get user inputs
    company_name = input("Enter the Company Name to prospect: ")
    my_product = input("Describe your product/service in one sentence: ")
    
    if not company_name or not my_product:
        print("Company name and product description are required.")
        return

    # 2. Agent performs research
    # This calls the first function
    research_findings = agent.research_company(company_name)
    
    print("\n--- Research Findings ---")
    print(research_findings)
    print("-------------------------\n")

    # 3. Agent drafts email
    # This calls the second function
    email_draft = agent.draft_email(company_name, research_findings, my_product)
    
    if email_draft:
        print("\n--- ✅ Generated Email Draft ---")
        print(email_draft)
        print("--------------------------------\n")
        
        # 4. Save the draft to a file
        try:
            # Create a clean filename
            filename = f"email_for_{company_name.lower().replace(' ', '_').replace('.', '')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(email_draft)
            print(f"Draft saved to {filename}")
        except Exception as e:
            print(f"Error saving file: {e}")
            
    else:
        print("Sorry, I couldn't generate an email draft.")


if __name__ == "__main__":
    main()
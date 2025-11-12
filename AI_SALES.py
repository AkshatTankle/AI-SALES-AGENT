import os
import google.generativeai as genai
from dotenv import load_dotenv
# We are using this library
from googlesearch import search
import time

class SalesAgent:
    """
    An agent that researches a company and drafts a personalized email.
    It has two tools:
    1. research_company: To find info using Google Search.
    2. draft_email: To write an email using an LLM.
    """
    
    def __init__(self):
        """
        Initializes the agent by loading the API key and setting up the model.
        """
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file")
            
        genai.configure(api_key=api_key)
        # Use the latest model alias
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def research_company(self, company_name):
        """
        Tool 1: Researches a company using Google Search.
        Returns a string of the top 3 search results.
        """
        print(f"🕵️  Researching {company_name}...")
        try:
            #
            # --- THIS IS THE CORRECTED CODE ---
            # These are the correct arguments for the 'googlesearch-python' library
            #
            search_results = list(search(
                company_name, 
                num_results=3,      # Correct argument for number of results
                sleep_interval=1    # Correct argument for a polite pause
            ))
            
            if not search_results:
                print("--- No search results found. ---")
                return f"No search results found for {company_name}."

            # Join the first 3 results
            return "\n".join(search_results[:3])
            
        except Exception as e:
            print(f"Error during search: {e}")
            # Fallback in case of search error (like a 429 block)
            return f"Could not perform search. Assumed {company_name} is a leader in its industry."

    def draft_email(self, company_name, research_findings, my_product):
        """
        Tool 2: Drafts a personalized email using the LLM.
        """
        print("🤖 Drafting personalized email...")
        
        prompt = f"""
        You are an expert AI Sales Development Representative (SDR).
        Your task is to write a short, personalized, and compelling cold email.

        **My Product/Service:**
        {my_product}

        **Prospect Information:**
        - Company Name: {company_name}
        - My Research (Top Google Results):
        {research_findings}

        **Instructions:**
        1.  Start with a specific, personalized compliment or observation based *only* on the research findings.
        2.  If the research failed (e.g., "No search results found" or "Could not perform search"), use a more generic but professional opening.
        3.  Briefly connect their company's focus to the problem my product solves.
        4.  Keep the email under 100 words.
        5.  End with a single, clear call-to-action (e.g., asking for a 15-minute call).
        
        **Email Draft:**
        Subject: 
        
        Body:
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating content: {e}")
            return None
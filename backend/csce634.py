import os
import requests
from openai import OpenAI

# --- Configuration ---
# 1. OpenAI API Key
OPENAI_API_KEY = "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"  # REPLACE with your actual OpenAI API Key

# 2. Tavily API Key (Get one for free at https://tavily.com)
# This is a stable replacement for DuckDuckGo
TAVILY_API_KEY = "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" # REPLACE with your actual Tavily API Key

# Initialize OpenAI client explicitly
client = OpenAI(api_key=OPENAI_API_KEY)

def search_web(query):
    """
    Step 1: Search the web using Tavily API.
    Tavily is optimized for LLMs and returns clean text context.
    
    Args:
        query (str): The user's search query.
        
    Returns:
        str: A formatted string containing the search results.
    """
    print(f"🔍 Searching the web for: '{query}' ...")
    
    # Tavily API endpoint
    url = "https://api.tavily.com/search"
    
    # Request payload
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic", # or "advanced" for deeper search
        "include_answer": False,
        "max_results": 3
    }

    try:
        # distinct from DuckDuckGo, we use standard HTTP request here
        response = requests.post(url, json=payload)
        response.raise_for_status() # Check for HTTP errors
        
        data = response.json()
        results = data.get("results", [])
        
        if not results:
            return "No search results found."

        # Format the results
        context_text = ""
        for idx, result in enumerate(results):
            title = result.get('title', 'No Title')
            content = result.get('content', 'No Content')
            url = result.get('url', '#')
            context_text += f"--- Source {idx+1} ---\nTitle: {title}\nContent: {content}\nURL: {url}\n\n"
            
        return context_text

    except Exception as e:
        print(f"Error during search: {e}")
        return "Search service is currently unavailable."

def generate_response(user_query):
    """
    Step 2: Combine the user query with the search context 
    and send it to gpt-4o-mini for a final response.
    """
    # A. Get search context
    search_context = search_web(user_query)
    
    # B. Construct the System Prompt
    system_prompt = (
        "You are a helpful AI assistant. "
        "Please answer the user's question using the provided [Search Results] as context. "
        "If the search results contain URLs, please cite them in your answer where appropriate."
        "Pretend you are helping a dispatcher help the caller"
    )
    
    # C. Construct the User Message
    user_message_content = f"""
    [Search Results]:
    {search_context}

    [User Question]:
    {user_query}
    """

    print("🤖 Generating response with gpt-4o-mini...")

    try:
        # D. Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message_content}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error communicating with OpenAI API: {e}"

# --- Main Execution Block ---
if __name__ == "__main__":
    # Example input text
    input_text = "I am trapped in the car, how to save myself?"
    
    # Run the function
    final_answer = generate_response(input_text)
    
    print("\n" + "="*40)
    print("💡 Response from gpt-4o-mini:")
    print("="*40)
    print(final_answer)
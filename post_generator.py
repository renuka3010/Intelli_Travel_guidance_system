from llm_helper import llm

def generate_travel_guidance(query, pdf_data, weather_data=None, chat_history=None):
    """
    Generate chatbot response based on user query, PDF data, weather info, and chat history.
    """
    # Find relevant content in the PDF data
    relevant_data = find_relevant_content(query, pdf_data)

    # Build LLM prompt
    history_context = ""
    if chat_history:
        history_context = "\n".join([f"User: {h['user']}\nChatbot: {h['bot']}" for h in chat_history])

    if relevant_data:
        prompt = f"""
        This is a conversation with a travel assistant. Use the context below to answer the user's question.
        
        Chat History:
        {history_context}

        User's Query: "{query}"

        Relevant PDF Data:
        {relevant_data[:1500]}  # Limit token size

        {f"The current weather is: {weather_data['temperature']}°C with {weather_data['weather']}." if weather_data else ""}
        """
    else:
        prompt = f"""
        This is a conversation with a travel assistant. Use the context below to answer the user's question.

        Chat History:
        {history_context}

        User's Query: "{query}"

        No relevant PDF data is available. Provide an expert recommendation.
        {f"The current weather is: {weather_data['temperature']}°C with {weather_data['weather']}." if weather_data else ""}
        """
    
    # Call LLM
    response = llm.invoke(prompt)
    return response.content

def find_relevant_content(query, pdf_data):
    """Search for relevant content in the PDF data."""
    keywords = query.lower().split()
    relevant_lines = [line for line in pdf_data.split("\n") if any(keyword in line.lower() for keyword in keywords)]
    return "\n".join(relevant_lines) if relevant_lines else None
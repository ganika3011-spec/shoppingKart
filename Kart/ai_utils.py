import google.generativeai as genai
from decouple import config
import logging

logger = logging.getLogger(__name__)

# Configure Gemini API
GOOGLE_API_KEY = config('GOOGLE_API_KEY', default='')
genai.configure(api_key=GOOGLE_API_KEY)

def get_gemini_response(prompt, model_name="gemini-pro-latest"):
    """
    General function to get a response from Gemini with fallback models.
    """
    if not GOOGLE_API_KEY:
        return "AI features are currently disabled. Please configure your GOOGLE_API_KEY in the .env file."
    
    # List of models to try in order
    models_to_try = [model_name, "gemini-1.5-flash", "gemini-pro", "gemini-flash-latest"]
    
    last_error = ""
    for model_id in models_to_try:
        try:
            model = genai.GenerativeModel(model_id)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            last_error = str(e)
            if "429" in last_error or "quota" in last_error.lower() or "not found" in last_error.lower():
                logger.warning(f"Issue with model {model_id}: {last_error}. Trying next fallback...")
                continue
            logger.error(f"Error with model {model_id}: {last_error}")
            break # If it's a significant error, stop
            
    return f"Sorry, I encountered a quota or model access issue. Error: {last_error}. Please ensure your API key has access to Gemini models in the Google AI Studio."

def generate_product_description(product_name, category_name):
    """
    Generates a professional product description.
    """
    prompt = f"Create a compelling and professional product description for a product named '{product_name}' in the category '{category_name}'. The description should be suitable for an e-commerce website and approximately 100-150 words long."
    return get_gemini_response(prompt)

def get_shopping_assistant_response(user_query, product_context):
    """
    Generates a response for the shopping assistant chatbot.
    """
    prompt = f"""
    You are a helpful and friendly AI Shopping Assistant for 'shoppingKart', an online store.
    
    Context:
    Available Products: {product_context}
    
    Instructions:
    - Answer user questions based on the provided product context.
    - If a user is looking for something, suggest relevant products from the context.
    - If you don't know the answer, politely say you don't have that information.
    - Keep responses concise and engaging.
    - Use markdown for formatting.
    
    User Query: {user_query}
    """
    return get_gemini_response(prompt)

def get_review_summary(product_name, reviews):
    """
    Generates a concise summary of product reviews.
    """
    if not reviews:
        return "Not enough reviews yet to generate a summary."
    
    reviews_text = "\n".join([f"- Rating {r.rating}/5: {r.subject} - {r.review}" for r in reviews])
    
    prompt = f"""
    You are an expert e-commerce analyst. Summarize the customer reviews for the product '{product_name}'.
    
    Reviews:
    {reviews_text}
    
    Instructions:
    - Provide a concise summary (2-3 sentences max).
    - Highlight the main positive and negative points mentioned by customers.
    - Start with a clear heading like "What customers are saying:".
    - Use a friendly and helpful tone.
    - If there are conflicting opinions, mention that.
    """
    return get_gemini_response(prompt)

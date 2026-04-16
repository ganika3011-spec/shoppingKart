from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Product
from Kart.ai_utils import get_shopping_assistant_response
import json

@csrf_exempt
def chatbot_api(request):
    """
    API endpoint for the AI chatbot.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_query = data.get('messages', [{}])[-1].get('text', '')
            
            if not user_query:
                return JsonResponse({'status': 'error', 'message': 'Empty message'}, status=400)
            
            # Fetch some product context to provide to AI
            # In a real app, we might use vector search, but here we'll just take the top 10 available products
            # or filter based on simple keyword match if possible.
            products = Product.objects.filter(is_available=True)[:10]
            product_context = "\n".join([f"- {p.product_name} (${p.price}): {p.description[:100]}..." for p in products])
            
            ai_response = get_shopping_assistant_response(user_query, product_context)
            
            return JsonResponse({
                'status': 'success',
                'response': ai_response
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

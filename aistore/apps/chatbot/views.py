from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from apps.store.models import Product, Category

@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        chat_history = request.session.get('chat_history', [])
        data = json.loads(request.body)
        message = data.get('message', '').lower()
        response_message = ''

        if 'hello' in message or 'hi' in message:
            response_message = "Hello! I'm your AiShop assistant. How can I help you today? You can ask me about our products, categories, or specific product details."
        elif 'product' in message:
            products = Product.objects.all()
            if 'list' in message or 'show' in message:
                if products:
                    response_message = "Of course! Here are some of our popular products:\n"
                    for product in products[:4]:
                        response_message += f"- {product.title}\n"
                    response_message += "\nIs there a specific product you'd like to know more about?"
                else:
                    response_message = "We currently don't have any products listed. Please check back later!"
            else:
                response_message = "I can tell you about our products. Would you like to see a list?"
        elif 'category' in message:
            categories = Category.objects.all()
            if categories:
                response_message = "We have a variety of categories to choose from:\n"
                for category in categories:
                    response_message += f"- {category.title}\n"
                response_message += "\nWhich category are you interested in?"
            else:
                response_message = "It seems we don't have any categories at the moment. Sorry about that!"
        else:
            # Check if the user is asking about a specific product from the history
            product_mentioned = None
            for past_message in reversed(chat_history):
                if 'products' in past_message['response']:
                    # Simple check if a product title is in the user's message
                    products = Product.objects.all()
                    for p in products:
                        if p.title.lower() in message:
                            product_mentioned = p
                            break
                    break

            if product_mentioned:
                response_message = f"Ah, the {product_mentioned.title}! It's priced at ${product_mentioned.price:.2f}. "
                if product_mentioned.description:
                    response_message += f"Here's a bit about it: {product_mentioned.description}"
                else:
                    response_message += "A great choice!"
            else:
                response_message = "I'm not sure I understand. Could you rephrase? I can help with products, categories, and pricing."

        chat_history.append({'user': message, 'response': response_message})
        request.session['chat_history'] = chat_history

        return JsonResponse({'response': response_message})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

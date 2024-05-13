from django.http import JsonResponse
from .models import Customer

def process_chunk(request):
    if request.method == 'POST':
        data = request.json
        chunk = data.get('chunk')

        if chunk:
            transactions = chunk.get('transactions', [])
            process_transactions(transactions)
            return JsonResponse({'message': 'Chunk processed successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Chunk data missing'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def process_transactions(transactions):
    for transaction in transactions:
        customer_id = transaction.get('customer')
        value = transaction.get('value')
        customer = Customer.objects.get(pk=customer_id)
        if customer.balance >= value:
            customer.balance -= value
            customer.save()
        else:
            # Log the transaction if the customer doesn't have enough balance
            print(f"Transaction logged: Customer {customer_id} doesn't have enough balance for value {value}.")

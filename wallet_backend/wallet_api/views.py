from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Transaction, Chunk
from .serializers import CustomerSerializer, TransactionSerializer, ChunkSerializer



# @api_view(['POST'])
# def transaction_view(request):
#     if request.method == 'POST':
#         transactions = request.data.get('transactions')
#         chunks = split_transactions(transactions)
#         for chunk_data in chunks:
#             serializer = ChunkSerializer(data=chunk_data)

#             if serializer.is_valid():
#                 print("serializer is saved")
#                 serializer.save()

#             if not serializer.is_valid():
#                 print(serializer.errors)

#         return Response("Transactions processed", status=status.HTTP_201_CREATED)

# def split_transactions(transactions):
#     sorted_transactions = sorted(transactions, key=lambda x: (x['value'], -x['latency']), reverse=True)
#     chunks = []
#     chunk = []
#     chunk_value = 0
#     chunk_latency = 1000

#     for transaction in sorted_transactions:
#         if chunk_value + transaction['value'] <= chunk_latency:
#             chunk.append(transaction)
#             chunk_value += transaction['value']
#         else:
#             chunks.append({'transactions': chunk, 'total_value': chunk_value})
#             chunk = [transaction]
#             chunk_value = transaction['value']

#     if chunk:
#         chunks.append({'transactions': chunk, 'total_value': chunk_value})

#     return chunks


@api_view(['POST'])
def transaction_view(request):
    if request.method == 'POST':
        transactions = request.data.get('transactions')
        chunks = split_transactions(transactions)
        serialized_chunks = []

        for chunk_data in chunks:
            serializer = ChunkSerializer(data=chunk_data)
            if serializer.is_valid():
                serialized_chunk = serializer.save()
                serialized_chunks.append(serialized_chunk)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response("Transactions processed", status=status.HTTP_201_CREATED)

def split_transactions(transactions):
    sorted_transactions = sorted(transactions, key=lambda x: (x['value'], -x['latency']), reverse=True)
    chunks = []
    chunk = []
    chunk_value = 0
    chunk_latency = 1000

    for transaction in sorted_transactions:

        transaction_value = float(transaction['value'])
        if chunk_value + transaction_value <= chunk_latency:
            chunk.append(transaction)
            chunk_value += transaction_value
        else:
            chunks.append({'transactions': chunk, 'total_value': chunk_value})
            chunk = [transaction]
            chunk_value = transaction['value']

    if chunk:
        chunks.append({'transactions': chunk, 'total_value': chunk_value})

    return chunks


@api_view(['POST'])
def print_chunk(request):
    if request.method == 'POST':
        chunks = request.data.get('chunks', None)  # Retrieve the chunks data from request data
        if chunks is None:
            return Response("Chunks data is missing.", status=400)  # Return an error response if chunks data is missing

        if not isinstance(chunks, list):
            return Response("Chunks data is not in the correct format.", status=400)  # Return an error response if chunks data is not in the correct format

        print("0000000000")
        for i, chunk in enumerate(chunks, start=1):
            print("start")
            print(f"Chunk {i}:")
            print("Transactions:", chunk.get('transactions'))
            print("Total value:", chunk.get('total_value'))
            print("Time left:", chunk.get('time_left'))
            print()
            print("end")  

        return Response("Chunks printed successfully.", status=200)

# def print_chunks(chunks):
#     for i, chunk in enumerate(chunks, start=1):
#         print(f"chunk {i}:")
#         print(f"transactions: {chunk['transactions']}")
#         print(f"total value: {chunk['total_value']}")
#         print(f"time left: {chunk['time_left']}\n")



@api_view(['GET', 'DELETE', 'PATCH'])
def customer_detail_view(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import Customer, Transaction, Chunk
# from .serializers import CustomerSerializer, TransactionSerializer, ChunkSerializer

# class TransactionView(APIView):
#     def post(self, request):
#         transactions = request.data.get('transactions')
#         chunks = self.split_transactions(transactions)
#         for chunk_data in chunks:
#             serializer = ChunkSerializer(data=chunk_data)
#             if serializer.is_valid():
#                 serializer.save()
#         return Response("Transactions processed", status=status.HTTP_201_CREATED)

#     def split_transactions(self, transactions):
#         sorted_transactions = sorted(transactions, key=lambda x: (x['value'], -x['latency']), reverse=True)
#         chunks = []
#         chunk = []
#         chunk_value = 0
#         chunk_latency = 1000

#         for transaction in sorted_transactions:
#             if chunk_value + transaction['value'] <= chunk_latency:
#                 chunk.append(transaction)
#                 chunk_value += transaction['value']
#             else:
#                 chunks.append({'transactions': chunk, 'total_value': chunk_value})
#                 chunk = [transaction]
#                 chunk_value = transaction['value']

#         if chunk:
#             chunks.append({'transactions': chunk, 'total_value': chunk_value})

#         return chunks

# class CustomerDetailView(APIView):
#     def get(self, request, pk):
#         customer = Customer.objects.get(pk=pk)
#         serializer = CustomerSerializer(customer)
#         return Response(serializer.data)

#     def delete(self, request, pk):
#         customer = Customer.objects.get(pk=pk)
#         customer.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def patch(self, request, pk):
#         customer = Customer.objects.get(pk=pk)
#         serializer = CustomerSerializer(customer, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

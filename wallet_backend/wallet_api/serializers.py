from rest_framework import serializers
from .models import Customer, Transaction, Chunk

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'balance']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'customer', 'value', 'latency']

class ChunkSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True)

    class Meta:
        model = Chunk
        fields = ['id', 'transactions', 'total_value']

    def create(self, validated_data):
        transactions_data = validated_data.pop('transactions')
        chunk = Chunk.objects.create(**validated_data)
        for transaction_data in transactions_data:
            Transaction.objects.create(chunk=chunk, **transaction_data)
        return chunk

# class ChunkSerializer(serializers.ModelSerializer):
#     customer = serializers.IntegerField(source='customer_id') 
#     class Meta:
#         model = Chunk
#         fields = '__all__'
        # fields = ['transactions', 'total_value']
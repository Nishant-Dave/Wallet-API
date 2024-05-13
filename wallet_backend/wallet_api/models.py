from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    balance = models.FloatField(default=0.0)

class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    value = models.FloatField()
    latency = models.IntegerField()

class Chunk(models.Model):
    transactions = models.ManyToManyField(Transaction)
    total_value = models.FloatField()

# class Chunk(models.Model):
#     value = models.FloatField()
#     latency = models.IntegerField()
#     customer_id = models.IntegerField()  # Assuming customer_id is an IntegerField
#     total_value = models.FloatField()

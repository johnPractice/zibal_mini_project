from rest_framework import fields, serializers
from interaction.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    key = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['key', 'value', 'count']

    def get_key(self, obj):
        return obj.create_date.date()

    def get_value(self, obj):
        return obj.price

    def get_count(self, obj):
        return Transaction.objects.filter(create_date=obj.create_date).count()

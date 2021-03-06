from django.db import models
from utils.global_error_handling.custom_error import ServiceUnAvailable
# Create your models here.
# think simple
# this model is just record the transction for user who have gateway
# didn't record the user transaction for simply :)


def price_validator(value):
    if value < 0:
        raise ValueError('مقدار تراکنش نمی تواند عدد منفی باشد')


class Transaction(models.Model):
    # supose merchant id less than 20 character
    # default=django.utils.timezone.now
    create_date = models.DateTimeField(
        null=False, blank=False)
    merchantId = models.CharField(
        max_length=20, null=False, blank=False)
    price = models.IntegerField(
        blank=False, null=False, validators=[price_validator])

    class Meta:
        ordering = ['create_date']

    @staticmethod
    def get_daily_transaction(merchent):
        try:
            if merchent is None:
                return Transaction.objects.all()
            return Transaction.objects.filter(merchantId=merchent)

        except Exception as e:
            print(e)
            raise ServiceUnAvailable()

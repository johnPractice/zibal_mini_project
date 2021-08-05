from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from interaction.serializers import TransactionSerializer
from interaction.models import Transaction
from interaction.utils.calc_weak_number import week_number_of_month
from utils.global_error_handling.custom_error import BadRequestInput, ServiceUnAvailable
# 3 type for report
# daily --weakly -- monthly


def remove_key_value(dic, key):
    if key in dic:
        dic.pop(key)
    return dic


def daily_report(merchant_id, mode):
    transactions = Transaction.get_daily_transaction(merchant_id)
    transactions_serializers = TransactionSerializer(
        transactions, many=True)

    return{'type': 'daily',
           'report': [remove_key_value(data, mode) for data in transactions_serializers.data]}


def weakly_report(merchant_id, mode):
    transactions = Transaction.get_daily_transaction(merchant_id)
    transactions_serializers = TransactionSerializer(
        transactions, many=True)
    result = {}
    for data in transactions_serializers.data:
        key_dic = f"{data['key'].year}/{data['key'].month}--{week_number_of_month(data['key'])}"
        if key_dic not in result:
            result.update({key_dic: data[mode]})
        else:
            result[key_dic] += data[mode]
    return{'type': 'weakly',
           'report': result}


def monthly_report(merchant_id, mode):
    transactions = Transaction.get_daily_transaction(merchant_id)
    transactions_serializers = TransactionSerializer(
        transactions, many=True)
    result = {}
    for data in transactions_serializers.data:
        key_dic = f"{data['key'].year}/{data['key'].month}"
        if key_dic not in result:
            result.update({key_dic: data[mode]})
        else:
            result[key_dic] += data[mode]
    return{'type': 'monthly',
           'report': result}


switch_type = {
    'daily': daily_report,
    'weakly': weakly_report,
    'monthly': monthly_report
}


class GetReport(APIView):
    def get(self, request):
        try:
            MODE_VALID_VALUE = ['value', 'count']
            merchant_id = request.query_params.get('merchantId') or None
            type_parameter = request.query_params.get('type') or None
            mode_parameter = request.query_params.get('mode') or None
            if merchant_id is None or mode_parameter is None or merchant_id is None:
                raise BadRequestInput(
                    detail={'message': 'enter essentioal thing'})
            if mode_parameter not in MODE_VALID_VALUE:
                raise BadRequestInput(
                    detail={'message': 'mode parameter not in valid type'})
            result = switch_type[type_parameter](
                merchant_id, mode_parameter) if type_parameter in switch_type else None
            if result is None:
                return Response(data={'messsage': 'not valid type insert'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            raise e

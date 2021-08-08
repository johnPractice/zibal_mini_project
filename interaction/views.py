from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from interaction.serializers import TransactionSerializer
from interaction.models import Transaction
from interaction.utils.calc_weak_number import week_number_of_month
from utils.global_error_handling.custom_error import BadRequestInput
from interaction.utils.global_storage import get_value, set_item
import pickle
# 3 type for report
# daily --weakly -- monthly
MODE_VALID_VALUE = ['value', 'count']


# TODO:can check thie better :)
def check_data(data):
    result = []
    for d in data:
        check = False
        for r in result:
            if r['key'] == d['key']:
                check = True
        if check is True:
            for r in result:
                if r['key'] == d['key']:
                    if 'value' in d:
                        r['value'] = r['value']+d['value']
                    if 'count' in d:
                        r['count'] = r['count']+d['count']
        else:
            result.append(d)
    return result


def remove_key_value(dic, key):
    result = {}
    for k in key:
        result.update({k: dic[k]})
    return result


def represent_result(data, mode, weak):
    result = {}
    for d in data:
        key_dic = f"{d['key'].year}/{d['key'].month}"
        key_dic = key_dic + \
            f"--{week_number_of_month(d['key'])}" if weak is True else key_dic
        if key_dic not in result:
            result.update({key_dic: d[mode]})
        else:
            result[key_dic] += d[mode]
    return result


def daily_report(merchant_id, mode):
    get_data = get_value(f'{merchant_id}-daily')
    if mode == 'count':
        mode = ['count', 'key']
    else:
        mode = ['value', 'key']
    if get_data is not None:
        return{'type': 'daily',
               'report': [remove_key_value(data, mode) for data in get_data]}
    transactions = Transaction.get_daily_transaction(merchant_id)
    transactions_serializers = TransactionSerializer(
        transactions, many=True)
    data = transactions_serializers.data

    data = check_data(data)
    set_item(f'{merchant_id}-daily', data)
    return{'type': 'daily',
           'report': [remove_key_value(data, mode) for data in data]}


def weakly_report(merchant_id, mode):
    get_data = get_value(f'{merchant_id}-weakly')
    if get_data is not None:
        return{'type': 'weakly',
               'report': represent_result(get_data, mode, True)}
    transactions = Transaction.get_daily_transaction(merchant_id)
    transactions_serializers = TransactionSerializer(
        transactions, many=True)
    data = transactions_serializers.data
    set_item(f'{merchant_id}-weakly', data)
    result = represent_result(data, mode, True)
    return{'type': 'weakly',
           'report': result}


def monthly_report(merchant_id, mode):
    get_data = get_value(f'{merchant_id}-monthly')
    if get_data is not None:
        return{'type': 'monthly',
               'report': represent_result(get_data, mode, False)}
    transactions = Transaction.get_daily_transaction(merchant_id)
    transactions_serializers = TransactionSerializer(
        transactions, many=True)
    data = transactions_serializers.data
    set_item(f'{merchant_id}-monthly', data)
    result = represent_result(data, mode, False)
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
            merchant_id = request.query_params.get('merchantId') or None
            type_parameter = request.query_params.get('type') or None
            mode_parameter = request.query_params.get('mode') or None
            if type_parameter is None or mode_parameter is None:
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

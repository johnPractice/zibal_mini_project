global_dic = {}

# TODO:add function for  remove some item after x second


def set_item(key, value):
    if key not in global_dic:
        global_dic.update({key: value})
    else:
        global_dic[key] = value
    return True


def get_value(key):
    if key in global_dic:
        return global_dic[key]
    return None

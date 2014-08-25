def filter_by_type(item_list, type):
    return [item for item in item_list if isinstance(item, type)]

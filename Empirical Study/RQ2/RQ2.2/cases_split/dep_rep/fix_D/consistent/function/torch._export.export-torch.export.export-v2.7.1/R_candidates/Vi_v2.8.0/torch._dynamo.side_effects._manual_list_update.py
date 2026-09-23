def _manual_list_update(list_from, list_to):
    list.clear(list_to)
    list.extend(list_to, list_from)

def _manual_dict_setitem(dict_from, dict_to, mro_index):
    # Carefully calls the dict or OrderedDict `clear` or `__setitem__`. We have
    # to be careful because we don't want to trigger the user defined object
    # setitem or clear. The mro_index is used to find the dict/OrderedDict from
    # the class mro.
    dict_class = type(dict_to).__mro__[mro_index]
    dict_class.clear(dict_to)
    for k, v in dict_from.items():
        dict_class.__setitem__(dict_to, k, v)

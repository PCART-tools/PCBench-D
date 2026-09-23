def get_nn_mod_test_name(**kwargs):
    name = get_nn_module_name_from_kwargs(**kwargs)
    test_name = name
    if 'desc' in kwargs:
        test_name = "{}_{}".format(test_name, kwargs['desc'])
    return 'test_nn_{}'.format(test_name)

def compute_module_name(test_params_dict):
    fullname = test_params_dict.get('fullname', None)
    if fullname:
        module_name = fullname.split('_')[0]
    else:
        module_name = test_params_dict.get('module_name')
    return module_name

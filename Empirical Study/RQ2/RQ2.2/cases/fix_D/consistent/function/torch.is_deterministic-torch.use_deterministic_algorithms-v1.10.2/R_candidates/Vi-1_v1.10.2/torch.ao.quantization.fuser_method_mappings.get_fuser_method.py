def get_fuser_method(op_list, additional_fuser_method_mapping=None):
    ''' Get fuser method for the given list of module types,
    return None if fuser method does not exist
    '''
    if additional_fuser_method_mapping is None:
        additional_fuser_method_mapping = dict()
    all_mappings = get_combined_dict(DEFAULT_OP_LIST_TO_FUSER_METHOD,
                                     additional_fuser_method_mapping)
    fuser_method = all_mappings.get(op_list, None)
    assert fuser_method is not None, "did not find fuser method for: {} ".format(op_list)
    return fuser_method

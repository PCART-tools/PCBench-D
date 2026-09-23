def unwrap_if_wrapper(fn):
    return unwrap_with_attr_name_if_wrapper(fn)[0]

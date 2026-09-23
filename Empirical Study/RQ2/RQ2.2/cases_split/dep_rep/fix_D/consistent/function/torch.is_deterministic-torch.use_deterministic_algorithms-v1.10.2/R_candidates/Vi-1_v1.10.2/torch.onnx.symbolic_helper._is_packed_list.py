def _is_packed_list(list_value):
    return _is_value(list_value) and list_value.node().kind() == "prim::ListConstruct"

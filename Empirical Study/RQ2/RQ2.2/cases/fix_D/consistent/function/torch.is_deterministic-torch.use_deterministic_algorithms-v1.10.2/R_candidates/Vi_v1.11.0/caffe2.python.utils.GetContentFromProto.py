def GetContentFromProto(obj, function_map):
    """Gets a specific field from a protocol buffer that matches the given class
    """
    for cls, func in viewitems(function_map):
        if type(obj) is cls:
            return func(obj)

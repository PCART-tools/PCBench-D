def GetContentFromProtoString(s, function_map):
    for cls, func in viewitems(function_map):
        try:
            obj = TryReadProtoWithClass(cls, s)
            return func(obj)
        except DecodeError:
            continue
    else:
        raise DecodeError("Cannot find a fit protobuffer class.")

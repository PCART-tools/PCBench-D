def _ProtoMapGet(field, key):
    """
    Given the key, get the value of the repeated field.
    Helper function used by protobuf since it doesn't have map construct
    """
    for v in field:
        if v.key == key:
            return v.value
    return None

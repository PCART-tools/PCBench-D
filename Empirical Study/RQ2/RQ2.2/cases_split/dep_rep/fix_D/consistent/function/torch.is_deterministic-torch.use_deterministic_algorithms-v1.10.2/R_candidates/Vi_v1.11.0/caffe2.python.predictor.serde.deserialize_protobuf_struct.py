def deserialize_protobuf_struct(serialized_protobuf, struct_type):
    deser = struct_type()
    deser.ParseFromString(serialized_protobuf)
    return deser

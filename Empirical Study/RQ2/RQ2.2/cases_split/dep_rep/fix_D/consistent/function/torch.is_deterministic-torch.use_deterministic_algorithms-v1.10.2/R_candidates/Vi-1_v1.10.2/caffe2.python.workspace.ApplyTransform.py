def ApplyTransform(transform_key, net):
    """Apply a Transform to a NetDef protobuf object, and returns the new
    transformed NetDef.

    Inputs:
      transform_key: the name of the transform, as it is stored in the registry
      net: a NetDef protobuf object
    Returns:
      Transformed NetDef protobuf object.
    """
    transformed_net = caffe2_pb2.NetDef()
    transformed_str = C.apply_transform(
        str(transform_key).encode('utf-8'),
        net.SerializeToString(),
    )
    transformed_net.ParseFromString(transformed_str)
    return transformed_net

def InferShapesAndTypes(nets, blob_dimensions=None, nets_proto=False,
                        blob_types=None):
    """Infers the shapes and types for the specified nets.

    Inputs:
      nets: the list of nets
      blob_dimensions (optional): a dictionary of blobs and their dimensions.
          If not specified, the workspace blobs are used.
      nets_proto (optional): a boolean flag indicating whether the protobuffer
          representation is passed to the routine.
    Returns:
      A tuple of (shapes, types) dictionaries keyed by blob name.
    """
    if nets_proto:
        net_protos = [StringifyProto(n) for n in nets]
    else:
        net_protos = [StringifyProto(n.Proto()) for n in nets]
    if blob_dimensions is None:
        assert blob_types is None
        blobdesc_prototxt = C.infer_shapes_and_types_from_workspace(net_protos)
    elif blob_types is None:
        blobdesc_prototxt = C.infer_shapes_and_types_from_map(
            net_protos, blob_dimensions
        )
    else:
        blobdesc_prototxt = C.infer_shapes_and_types_from_map(
            net_protos, blob_dimensions, blob_types
        )
    blobdesc_proto = caffe2_pb2.TensorShapes()
    blobdesc_proto.ParseFromString(blobdesc_prototxt)
    shapes = {}
    types = {}
    for ts in blobdesc_proto.shapes:
        if not ts.unknown_shape:
            shapes[ts.name] = list(ts.dims)
            types[ts.name] = ts.data_type

    return (shapes, types)

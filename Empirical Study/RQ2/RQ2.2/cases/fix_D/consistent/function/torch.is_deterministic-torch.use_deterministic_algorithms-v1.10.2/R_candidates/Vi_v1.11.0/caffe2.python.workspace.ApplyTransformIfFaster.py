def ApplyTransformIfFaster(transform_key, net, init_net, **kwargs):
    """Apply a Transform to a NetDef protobuf object, and returns the new
    transformed NetDef, only if it runs faster than the original.

    The runs are performed on the current active workspace (gWorkspace).
    You should initialize that workspace before making a call to this function.

    Inputs:
      transform_key: the name of the transform, as it is stored in the registry
      net: a NetDef protobuf object
      init_net: The net to initialize the workspace.
      warmup_runs (optional):
        Determines how many times the net is run before testing.
        Will be 5 by default.
      main_runs (optional):
        Determines how many times the net is run during testing.
        Will be 10 by default.
      improvement_threshold (optional):
        Determines the factor which the new net needs to be faster
        in order to replace the old. Will be 1.01 by default.

    Returns:
      Either a Transformed NetDef protobuf object, or the original netdef.
    """

    warmup_runs = kwargs['warmup_runs'] if 'warmup_runs' in kwargs else 5
    main_runs = kwargs['main_runs'] if 'main_runs' in kwargs else 10
    improvement_threshold = kwargs['improvement_threshold'] \
        if 'improvement_threshold' in kwargs else 1.01

    transformed_net = caffe2_pb2.NetDef()
    transformed_str = C.apply_transform_if_faster(
        str(transform_key).encode('utf-8'),
        net.SerializeToString(),
        init_net.SerializeToString(),
        warmup_runs,
        main_runs,
        float(improvement_threshold),
    )
    transformed_net.ParseFromString(transformed_str)
    return transformed_net

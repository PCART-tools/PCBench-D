def load_from_db(filename, db_type, device_option=None, *args, **kwargs):
    # global_init_net in meta_net_def will load parameters from
    # predictor_constants.PREDICTOR_DBREADER
    create_db = core.CreateOperator(
        'CreateDB', [],
        [core.BlobReference(predictor_constants.PREDICTOR_DBREADER)],
        db=filename, db_type=db_type)
    assert workspace.RunOperatorOnce(create_db), (
        'Failed to create db {}'.format(filename))

    # predictor_constants.META_NET_DEF is always stored before the parameters
    load_meta_net_def = core.CreateOperator(
        'Load',
        [core.BlobReference(predictor_constants.PREDICTOR_DBREADER)],
        [core.BlobReference(predictor_constants.META_NET_DEF)])
    assert workspace.RunOperatorOnce(load_meta_net_def)

    blob = workspace.FetchBlob(predictor_constants.META_NET_DEF)
    meta_net_def = serde.deserialize_protobuf_struct(
        blob if isinstance(blob, bytes)
        else str(blob).encode('utf-8'),
        metanet_pb2.MetaNetDef)

    if device_option is None:
        device_option = scope.CurrentDeviceScope()

    if device_option is not None:
        # Set the device options of all loaded blobs
        for kv in meta_net_def.nets:
            net = kv.value
            for op in net.op:
                op.device_option.CopyFrom(device_option)

    return meta_net_def

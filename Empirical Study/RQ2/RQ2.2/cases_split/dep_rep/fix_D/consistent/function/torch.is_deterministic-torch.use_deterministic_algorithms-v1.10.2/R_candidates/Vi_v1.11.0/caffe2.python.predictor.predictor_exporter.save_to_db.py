def save_to_db(db_type, db_destination, predictor_export_meta, use_ideep=False,
               *args, **kwargs):
    meta_net_def = get_meta_net_def(predictor_export_meta, db_type=db_type)
    device_type = caffe2_pb2.IDEEP if use_ideep else caffe2_pb2.CPU
    with core.DeviceScope(core.DeviceOption(caffe2_pb2.CPU)):
        workspace.FeedBlob(
            predictor_constants.META_NET_DEF,
            serde.serialize_protobuf_struct(meta_net_def)
        )

    blobs_to_save = [predictor_constants.META_NET_DEF] + \
        predictor_export_meta.parameters

    op = core.CreateOperator(
        "Save",
        blobs_to_save, [],
        device_option = core.DeviceOption(device_type),
        absolute_path=True,
        db=db_destination, db_type=db_type,
        **kwargs
    )

    workspace.RunOperatorOnce(op)

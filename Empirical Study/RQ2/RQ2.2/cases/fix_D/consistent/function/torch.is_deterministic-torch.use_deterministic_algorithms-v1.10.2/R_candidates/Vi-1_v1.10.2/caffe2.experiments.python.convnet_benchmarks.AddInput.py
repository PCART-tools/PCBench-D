def AddInput(model, batch_size, db, db_type):
    """Adds the data input part."""
    data_uint8, label = model.TensorProtosDBInput(
        [], ["data_uint8", "label"], batch_size=batch_size,
        db=db, db_type=db_type
    )
    data = model.Cast(data_uint8, "data_nhwc", to=core.DataType.FLOAT)
    data = model.NHWC2NCHW(data, "data")
    data = model.Scale(data, data, scale=float(1. / 256))
    data = model.StopGradient(data, data)
    return data, label

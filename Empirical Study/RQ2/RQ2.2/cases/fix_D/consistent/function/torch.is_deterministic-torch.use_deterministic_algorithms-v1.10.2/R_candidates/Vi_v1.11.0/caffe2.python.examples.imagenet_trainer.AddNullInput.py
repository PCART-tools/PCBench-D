def AddNullInput(model, reader, batch_size, img_size, dtype):
    '''
    The null input function uses a gaussian fill operator to emulate real image
    input. A label blob is hardcoded to a single value. This is useful if you
    want to test compute throughput or don't have a dataset available.
    '''
    suffix = "_fp16" if dtype == "float16" else ""
    model.param_init_net.GaussianFill(
        [],
        ["data" + suffix],
        shape=[batch_size, 3, img_size, img_size],
    )
    if dtype == "float16":
        model.param_init_net.FloatToHalf("data" + suffix, "data")

    model.param_init_net.ConstantFill(
        [],
        ["label"],
        shape=[batch_size],
        value=1,
        dtype=core.DataType.INT32,
    )

def mark_as_int8_layer(layer, dynamic_range):
    """
    Set the precision of a layer to int8 as well as the type of its first output.
    Also set the dynamic range of its first output.
    """
    if layer.type not in {trt.LayerType.SHUFFLE, trt.LayerType.CONCATENATION, trt.LayerType.CONSTANT, trt.LayerType.SHAPE}:
        layer.precision = trt.int8

    for i in range(layer.num_outputs):
        output_val = layer.get_output(i)
        output_val.dynamic_range = dynamic_range
        layer.set_output_type(i, trt.int8)

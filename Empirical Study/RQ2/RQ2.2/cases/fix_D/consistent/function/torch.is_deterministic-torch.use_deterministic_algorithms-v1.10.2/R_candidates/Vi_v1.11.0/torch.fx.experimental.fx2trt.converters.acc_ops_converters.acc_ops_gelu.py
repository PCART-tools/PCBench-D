@tensorrt_converter(acc_ops.gelu, no_implicit_batch_dim=True)
def acc_ops_gelu(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]
    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(
            f"GELU received input {input_val} that is not part "
            "of the TensorRT region!"
        )
    if network.has_implicit_batch_dimension:
        raise RuntimeError(
            "GeLU converter currently doesn't support implicit batch dimension"
        )

    plugin_name = "CustomGeluPluginDynamic"
    # type_id 0 for float32, 1 for  float16
    type_id = trt.PluginField("type_id", np.array(0, dtype=np.int32), trt.PluginFieldType.INT32)
    field_collection = TRTPluginFieldCollection([type_id])
    plugin_version = "1"

    plugin = get_trt_plugin(plugin_name, field_collection, plugin_version)

    layer = network.add_plugin_v2([input_val], plugin)
    set_layer_name(layer, target, name)
    return layer.get_output(0)

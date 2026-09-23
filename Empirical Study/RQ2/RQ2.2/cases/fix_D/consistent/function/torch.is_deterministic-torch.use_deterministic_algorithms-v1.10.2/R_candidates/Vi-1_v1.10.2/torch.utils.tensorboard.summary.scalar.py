def scalar(name, scalar, collections=None, new_style=False, double_precision=False):
    """Outputs a `Summary` protocol buffer containing a single scalar value.
    The generated Summary has a Tensor.proto containing the input Tensor.
    Args:
      name: A name for the generated node. Will also serve as the series name in
        TensorBoard.
      tensor: A real numeric Tensor containing a single value.
      collections: Optional list of graph collections keys. The new summary op is
        added to these collections. Defaults to `[GraphKeys.SUMMARIES]`.
      new_style: Whether to use new style (tensor field) or old style (simple_value
        field). New style could lead to faster data loading.
    Returns:
      A scalar `Tensor` of type `string`. Which contains a `Summary` protobuf.
    Raises:
      ValueError: If tensor has the wrong shape or type.
    """
    scalar = make_np(scalar)
    assert scalar.squeeze().ndim == 0, "scalar should be 0D"
    # python float is double precision in numpy
    scalar = float(scalar)
    if new_style:
        tensor = TensorProto(float_val=[scalar], dtype="DT_FLOAT")
        if double_precision:
            tensor = TensorProto(double_val=[scalar], dtype="DT_DOUBLE")

        plugin_data = SummaryMetadata.PluginData(plugin_name="scalars")
        smd = SummaryMetadata(plugin_data=plugin_data)
        return Summary(
            value=[
                Summary.Value(
                    tag=name,
                    tensor=tensor,
                    metadata=smd,
                )
            ]
        )
    else:
        return Summary(value=[Summary.Value(tag=name, simple_value=scalar)])

def _populate_tensor_meta(node: Node, output_spec: OutputSpecType) -> None:
    """
    Util function to populate tensor meta of output_spec based on node metadata.
    """
    if isinstance(node.meta["val"], Sequence):
        assert isinstance(output_spec, Sequence)
        for spec, fake_tensor in zip(output_spec, node.meta["val"]):
            assert spec is not None
            spec.tensor_meta = TensorMeta(
                shape=fake_tensor.shape,
                stride=fake_tensor.stride(),
                dtype=fake_tensor.dtype,
            )
    else:
        assert isinstance(output_spec, DTensorSpec)
        output_spec.tensor_meta = TensorMeta(
            shape=node.meta["val"].shape,
            stride=node.meta["val"].stride(),
            dtype=node.meta["val"].dtype,
        )

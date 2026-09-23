def _create_tensor_proto_with_external_data(
    tensor: torch.Tensor,
    name: str,
    location: str,
    basepath: str,
    dtype_override: onnx.TypeProto | None = None,  # type: ignore[name-defined]
) -> onnx.TensorProto:  # type: ignore[name-defined]
    """Create a TensorProto with external data from a PyTorch tensor.
    The external data is saved to os.path.join(basepath, location).

    Args:
        tensor: Tensor to be saved.
        name: Name of the tensor (i.e., initializer name in ONNX graph).
        location: Relative location of the external data file
            (e.g., "/tmp/initializers/weight_0" when model is "/tmp/model_name.onnx").
        basepath: Base path of the external data file (e.g., "/tmp/external_data" while model must be in "/tmp").


    Reference for ONNX's external data format:
        How to load?
        https://github.com/onnx/onnx/blob/5dac81ac0707bdf88f56c35c0a5e8855d3534673/onnx/external_data_helper.py#L187
        How to save?
        https://github.com/onnx/onnx/blob/5dac81ac0707bdf88f56c35c0a5e8855d3534673/onnx/external_data_helper.py#L43
        How to set ONNX fields?
        https://github.com/onnx/onnx/blob/5dac81ac0707bdf88f56c35c0a5e8855d3534673/onnx/external_data_helper.py#L88
    """
    # FIXME: Avoid importing onnx into torch.onnx.
    import onnx

    scalar_type = (
        jit_type_utils.JitScalarType.from_onnx_type(
            dtype_override.tensor_type.elem_type
        )
        if dtype_override is not None
        else jit_type_utils.JitScalarType.from_dtype(tensor.dtype)
    )

    # Checkpoints can be stored with a different dtype as the model expects because
    # the user script can explicitly cast the original type to something or maybe
    # PyTorch's type promotion might do it
    if dtype_override is not None and scalar_type.dtype() != tensor.dtype:
        tensor = tensor.to(scalar_type.dtype())

    tensor_proto = onnx.TensorProto()  # type: ignore[attr-defined]
    tensor_proto.name = name
    tensor_proto.data_type = scalar_type.onnx_type()  # type: ignore[assignment]

    tensor_proto.dims.extend(tensor.shape)
    tensor_proto.data_location = onnx.TensorProto.EXTERNAL  # type: ignore[attr-defined]

    # Settings for saving one tensor per file.
    # Offset is zero because there is no other tensor in the same file.
    key_value_pairs = {
        "location": location,
        "offset": 0,
        "length": tensor.untyped_storage().nbytes(),
    }
    for k, v in key_value_pairs.items():
        entry = tensor_proto.external_data.add()
        entry.key = k
        entry.value = str(v)

    # Actual path to write content of tensor.
    external_data_file_path = os.path.join(basepath, location)
    if os.path.exists(external_data_file_path):
        os.remove(external_data_file_path)

    # Create external data's folder if not exists.
    external_data_dir_path = os.path.dirname(external_data_file_path)
    if not os.path.exists(external_data_dir_path):
        # if the demo_folder directory is not present
        # then create it.
        os.makedirs(external_data_dir_path)

    # Create a fresh file.
    with open(external_data_file_path, "xb") as data_file:
        # No need to call "seek" because offset is 0.
        # data_file.seek(0)
        # Write tensor content to the file.
        data_file.write(tensor.numpy(force=True).tobytes())

    return tensor_proto

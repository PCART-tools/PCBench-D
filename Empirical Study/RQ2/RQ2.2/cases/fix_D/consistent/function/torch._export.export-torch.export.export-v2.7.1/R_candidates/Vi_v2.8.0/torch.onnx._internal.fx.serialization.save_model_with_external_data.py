def save_model_with_external_data(
    basepath: str,
    model_location: str,
    initializer_location: str,
    torch_state_dicts: tuple[dict | FileLike, ...],
    onnx_model: onnx.ModelProto,  # type: ignore[name-defined]
    rename_initializer: bool = False,
) -> None:
    """Load PyTorch tensors from files and add to "onnx_model" as external initializers.

    Output files:
        ONNX model file path:
        ONNX initializer folder: os.path.join(basepath, initializer_location)

    After running this function, you can do
        ort_sess = onnxruntime.InferenceSession(os.path.join(basepath, model_location))
    to execute the model.

    Arguments:
        basepath: Base path of the ONNX external data file (e.g., "/path/to/large_model/").
        model_location: Relative location of the ONNX model file.
            E.g., "model.onnx" so that the model file is saved to
            "<basepath>/model.onnx".
        initializer_location: Relative location of the ONNX initializer folder.
            E.g., "initializers" so that the initializers are saved to
            "<basepath>/initializers/".
            Note: When initializers are >2GB, must be the same as `model_location`.
        torch_state_dicts: Dictionaries or files which contain PyTorch tensors to be saved
            as ONNX initializers. For non-dict arguments, `torch.load` will be used to load them from file-like objects.
        onnx_model: ONNX model to be saved with external initializers.
            If an input name matches a tensor loaded from "torch_state_dicts",
            the tensor will be saved as that input's external initializer.
        rename_initializer: Replaces "." by "_" for all ONNX initializer names.
            Not needed by the official torch.onnx.dynamo_export. This is a hack
            for supporting `FXSymbolicTracer` tracer with fake tensor mode.
            In short, `FXSymbolicTracer` lifts FX parameters (self.linear_weight)
            as inputs (`def forward(self, linear_weight)`) and therefore, `.` cannot be used.
    """
    # FIXME: Avoid importing onnx into torch.onnx.
    import onnx

    initializers_to_be_deleted = {}  # Using dict because it is **ordered**
    existing_initializers = {
        k.name: idx for idx, k in enumerate(onnx_model.graph.initializer)
    }
    onnx_input_names = {input.name for input in onnx_model.graph.input}
    for el in torch_state_dicts:
        if isinstance(el, dict):
            # Useful for when state_dict is loaded with torch.load(..., mmap=True, map_location="cpu") by the user
            # Using torch.save wouldn't leverage mmap, leading to higher memory usage
            state_dict = el
        else:
            if isinstance(el, (str, os.PathLike)) and os.fspath(el).endswith(
                ".safetensors"
            ):
                state_dict = _convert_safetensors_to_torch_format(el)
            else:
                try:
                    # Loads checkpoint using memory-map on CPU to support really large models
                    # The underlying torch.UntypedStorage is memory mapped, so state_dict is lazy loaded
                    state_dict = torch.load(el, map_location="cpu", mmap=True)
                except (RuntimeError, ValueError) as e:
                    if "mmap can only be used with files saved with" in str(e) or (
                        isinstance(el, (io.IOBase, IO))
                        and el.readable()
                        and el.seekable()
                    ):
                        log.warning(
                            "Failed to load the checkpoint with memory-map enabled, retrying without memory-map."
                            "Consider updating the checkpoint with mmap by using torch.save() on PyTorch version >= 1.6."
                        )
                        if isinstance(el, (io.IOBase, IO)):
                            el.seek(0)  # torch.load from `try:` has read the file.
                        state_dict = torch.load(el, map_location="cpu")
                    else:
                        raise e

        for name, tensor in state_dict.items():
            if rename_initializer:
                # Basically, "transformer.attention.self.query.weight" is mapped
                # to "transformer_attention_self_query_weight" for mimicking the
                # name-modifying code in FX-to-ONNX exporter.
                # See function _replace_get_attr_with_placeholder for details.
                name = name.replace(".", "_")

            # This block tries to match the onnx initializer name with torch parameter/buffer
            #  e.g. A pytorch buffer 'transformer.h.0.attn.bias' can be named 'h.0.attn.bias' in a ONNX initializer
            # For each PyTorch tensor name loaded by torch.load,
            #  1.  Search its best match in ONNX model. E.g., the match of
            #       "transformer_attention_weight" could be "attention_weight".
            #  2.  Set "tensor" as the initializer of the matched ONNX input.
            #      E.g., "tensor" is stored as the initializer of "attention_weight".
            # Step 1 is required because sometimes, tensor names are stored with prefix the dictionary
            # loaded by torch.load.
            if name in onnx_input_names:
                # Same input name shouldn't be matched again
                onnx_input_names.remove(name)
            else:
                for onnx_input_name in onnx_input_names:
                    if onnx_input_name.endswith(name) or name.endswith(onnx_input_name):
                        # Find a match. Change name to the matched ONNX input name, so that we
                        # create initializer with the right ONNX name.
                        name = onnx_input_name
                        onnx_input_names.remove(onnx_input_name)
                        break

            relative_tensor_file_path = os.path.join(initializer_location, name)
            # Create one file per tensor.
            # tensor_proto.raw_data is stored to external file at
            # os.path.join(basepath, relative_tensor_file_path).
            model_input_types = {k.name: k.type for k in onnx_model.graph.input}

            # Mark for deletion - a replacement will be appended next
            if name in existing_initializers:
                initializers_to_be_deleted[existing_initializers[name]] = name
            tensor_proto = _create_tensor_proto_with_external_data(
                tensor,
                name,
                relative_tensor_file_path,
                basepath,
                model_input_types.pop(name, None),
            )
            # Add the tensor_proto to the ONNX model as an initializer with external data.
            onnx_model.graph.initializer.append(tensor_proto)
    # Remove old duplicated initializers, if any. delete in desc order to not invalidate deletion indices
    initializers_to_be_deleted = dict(
        sorted(initializers_to_be_deleted.items(), reverse=True)
    )
    for idx in initializers_to_be_deleted.keys():
        del onnx_model.graph.initializer[idx]

    # model_location should be a pure file name such as "file_name.onnx", not "folder/file_name.onnx".
    onnx.save(onnx_model, os.path.join(basepath, model_location))  # type: ignore[attr-defined]

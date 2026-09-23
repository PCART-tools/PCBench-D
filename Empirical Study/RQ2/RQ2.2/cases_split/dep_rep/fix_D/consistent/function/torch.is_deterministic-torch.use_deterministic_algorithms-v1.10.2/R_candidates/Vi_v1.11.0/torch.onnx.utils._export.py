def _export(model, args, f, export_params=True, verbose=False, training=None,
            input_names=None, output_names=None, operator_export_type=None,
            export_type=ExportTypes.PROTOBUF_FILE, opset_version=None,
            do_constant_folding=True, dynamic_axes=None, keep_initializers_as_inputs=None,
            fixed_batch_size=False, custom_opsets=None, add_node_names=True,
            onnx_shape_inference=True, export_modules_as_functions=False):

    if export_modules_as_functions and opset_version < 15:
        raise ValueError("`export_modules_as_functions` is not supported for `opset_version` < 15."
                         "This is because `opset_version` < 15 implies IR version < 8, which means "
                         "no local function support. ")
    export_modules_as_functions = _setup_trace_module_map(model, export_modules_as_functions)

    if isinstance(model, torch.nn.DataParallel):
        raise ValueError("torch.nn.DataParallel is not supported by ONNX "
                         "exporter, please use 'attribute' module to "
                         "unwrap model from torch.nn.DataParallel. Try "
                         "torch.onnx.export(model.module, ...)")
    global __IN_ONNX_EXPORT
    assert __IN_ONNX_EXPORT is False
    __IN_ONNX_EXPORT = True
    try:
        from torch.onnx.symbolic_helper import _set_onnx_shape_inference
        _set_onnx_shape_inference(onnx_shape_inference)

        from torch.onnx.symbolic_helper import _default_onnx_opset_version, _set_opset_version
        from torch.onnx.symbolic_helper import _set_operator_export_type
        if opset_version is None:
            opset_version = _default_onnx_opset_version
        if not operator_export_type:
            if torch.onnx.PYTORCH_ONNX_CAFFE2_BUNDLE:
                operator_export_type = OperatorExportTypes.ONNX_ATEN_FALLBACK
            else:
                operator_export_type = OperatorExportTypes.ONNX

        # By default, training=None, (which defaults to TrainingMode.EVAL),
        # which is good because running a model in training mode could result in
        # internal buffers getting updated, dropout getting applied, etc.
        # If you really know what you're doing, you can turn
        # training=TrainingMode.TRAINING or training=TrainingMode.PRESERVE,
        # (to preserve whatever the original training mode was.)
        _set_opset_version(opset_version)
        _set_operator_export_type(operator_export_type)
        with exporter_context(model, training):
            val_keep_init_as_ip = _decide_keep_init_as_input(keep_initializers_as_inputs,
                                                             operator_export_type,
                                                             opset_version)
            val_add_node_names = _decide_add_node_names(add_node_names, operator_export_type)
            val_do_constant_folding = _decide_constant_folding(do_constant_folding, operator_export_type, training)
            # Normally f can be a file-like object, but for large models, the external data format requires a
            # valid `model_file_location`. Code in export.cpp will enforce this.
            if isinstance(f, str):
                model_file_location = f
            else:
                model_file_location = str()
            args = _decide_input_format(model, args)
            if dynamic_axes is None:
                dynamic_axes = {}
            _validate_dynamic_axes(dynamic_axes, model, input_names, output_names)

            graph, params_dict, torch_out = \
                _model_to_graph(model, args, verbose, input_names,
                                output_names, operator_export_type,
                                val_do_constant_folding,
                                fixed_batch_size=fixed_batch_size,
                                training=training,
                                dynamic_axes=dynamic_axes)

            # TODO: Don't allocate a in-memory string for the protobuf
            defer_weight_export = export_type is not ExportTypes.PROTOBUF_FILE
            if custom_opsets is None:
                custom_opsets = {}

            torch._C._jit_pass_dce_allow_deleting_nodes_with_side_effects(graph)
            node_attr_to_name = {}  # type: ignore[var-annotated]
            if export_modules_as_functions is not None:
                # NOTE: cannot call DCE after this pass. DCE will remove function definition nodes.
                node_attr_to_name = torch._C._jit_pass_onnx_function_extraction(
                    graph, export_modules_as_functions, list(params_dict.keys()))
            if export_params:
                proto, export_map, val_use_external_data_format = graph._export_onnx(
                    params_dict, opset_version, dynamic_axes, defer_weight_export,
                    operator_export_type, not verbose, val_keep_init_as_ip, custom_opsets,
                    val_add_node_names, model_file_location, node_attr_to_name)
            else:
                proto, export_map, val_use_external_data_format = graph._export_onnx(
                    {}, opset_version, dynamic_axes, False, operator_export_type,
                    not verbose, val_keep_init_as_ip, custom_opsets, val_add_node_names,
                    model_file_location, node_attr_to_name)
            if export_type == ExportTypes.PROTOBUF_FILE:
                assert(len(export_map) == 0)
                with torch.serialization._open_file_like(f, "wb") as opened_file:
                    opened_file.write(proto)
            elif export_type in [ExportTypes.ZIP_ARCHIVE, ExportTypes.COMPRESSED_ZIP_ARCHIVE]:
                import zipfile
                compression = zipfile.ZIP_DEFLATED \
                    if export_type == ExportTypes.COMPRESSED_ZIP_ARCHIVE \
                    else zipfile.ZIP_STORED
                with zipfile.ZipFile(f, "w", compression=compression) as z:
                    z.writestr(ONNX_ARCHIVE_MODEL_PROTO_NAME, proto)
                    for k, v in export_map.items():
                        z.writestr(k, v)
            elif export_type == ExportTypes.DIRECTORY:
                import os
                if os.path.exists(f):
                    assert(os.path.isdir(f))
                else:
                    os.makedirs(f)

                model_proto_file = os.path.join(f, ONNX_ARCHIVE_MODEL_PROTO_NAME)
                with torch.serialization._open_file_like(model_proto_file, "wb") as opened_file:
                    opened_file.write(proto)

                for k, v in export_map.items():
                    weight_proto_file = os.path.join(f, k)
                    with torch.serialization._open_file_like(weight_proto_file, "wb") as opened_file:
                        opened_file.write(v)
            else:
                raise RuntimeError("Unknown export type")

            # The ONNX checker only works for ONNX graph. So if the operator_export_type is not ONNX,
            # we can skip this check.
            # If large model format export is enabled, proto will only contain data location instead of
            # raw data and _check_onnx_proto() will fail because it can only handle the raw ONNX proto
            # string in memory.
            if (operator_export_type is OperatorExportTypes.ONNX) and (not val_use_external_data_format):
                try:
                    _check_onnx_proto(proto)
                except RuntimeError as e:
                    raise CheckerError(e)
    finally:
        assert __IN_ONNX_EXPORT
        __IN_ONNX_EXPORT = False
        _reset_trace_module_map()
    return torch_out

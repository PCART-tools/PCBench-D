def preprocess(script_module: torch._C.ScriptObject, compile_spec: Dict[str, Tuple]):
    spec = compile_spec["forward"]
    forward_spec = _CompileSpec(*spec)
    mil_inputs = []
    inputs = []
    for index, input_spec in enumerate(forward_spec.inputs):
        input_spec = _TensorSpec(*input_spec)  # type: ignore[misc]
        name = "input_" + str(index)
        inputs.append([name, str(input_spec.dtype), str(input_spec.shape)])
        ml_type = _convert_to_mil_type(input_spec, name)
        mil_inputs.append(ml_type)
    model = torch.jit.RecursiveScriptModule._construct(script_module, lambda x: None)
    mlmodel = ct.convert(model, inputs=mil_inputs)
    spec = mlmodel.get_spec()
    output_specs = forward_spec.outputs
    assert len(spec.description.output) == len(output_specs)  # type: ignore[attr-defined]
    outputs = []
    for index, output_spec in enumerate(output_specs):
        output_spec = _TensorSpec(*output_spec)  # type: ignore[misc]
        name = spec.description.output[index].name  # type: ignore[attr-defined]
        outputs.append([name, str(output_spec.dtype), str(output_spec.shape)])
    mlmodel = ct.models.model.MLModel(spec)
    config = {
        "spec_ver": str(spec.specificationVersion),  # type: ignore[attr-defined]
        "backend": forward_spec.backend,
        "allow_low_precision": str(forward_spec.allow_low_precision),
    }
    metadata = {
        "coremltool_ver": mlmodel.user_defined_metadata[CT_METADATA_VERSION],
        "torch_ver": mlmodel.user_defined_metadata[CT_METADATA_SOURCE],
    }
    coreml_compile_spec = {
        "inputs": inputs,
        "outputs": outputs,
        "config": config,
        "metadata": metadata,
    }
    mlmodel = spec.SerializeToString()  # type: ignore[attr-defined]

    return {
        "model": mlmodel,
        "hash": str(hashlib.sha256(mlmodel).hexdigest()),
        "extra": json.dumps(coreml_compile_spec),
    }

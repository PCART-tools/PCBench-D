def create_forward_derivative(f: NativeFunction, formula: str, names: Tuple[str, ...]) -> ForwardDerivative:
    assert len(names) == 1, "Forward derivatives can define gradients for only one output at a time"
    var_name = names[0]
    var_type: Optional[Type] = None
    for r in f.func.returns:
        if r.name == var_name:
            var_type = r.type
            break
    # Handle default return names
    if var_type is None:
        if var_name == "result":
            assert len(f.func.returns) == 1
            var_type = f.func.returns[0].type
        else:
            res = re.findall(r"^result(\d+)$", var_name)
            if len(res) == 1:
                arg_idx = int(res[0])
                var_type = f.func.returns[arg_idx].type

    assert var_type is not None, "No matching output for forward derivative definition"
    return ForwardDerivative(
        formula=formula,
        var_name=var_name,
        var_type=var_type,
        required_inputs_fw_grad=None,
        required_inputs_primal=None,
        required_original_self_value=False,
        is_reusing_outplace_formula=False)

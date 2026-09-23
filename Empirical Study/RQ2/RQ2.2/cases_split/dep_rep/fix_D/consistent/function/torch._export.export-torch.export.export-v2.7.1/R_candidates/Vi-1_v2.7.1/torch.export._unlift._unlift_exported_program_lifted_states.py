def _unlift_exported_program_lifted_states(ep: ExportedProgram) -> torch.nn.Module:
    # TODO T206340015
    if ep.verifiers[0].dialect != "TRAINING":
        ep = _remove_effect_tokens(ep)
    new_gm = torch.fx.GraphModule(ep.graph_module, copy.deepcopy(ep.graph))
    _register_attrs_to_new_gm(new_gm, ep.graph_signature, ep.state_dict, ep.constants)
    forward_arg_names = (
        sig.forward_arg_names if (sig := ep.module_call_graph[0].signature) else None
    )
    lifted_inputs: list[Optional[str]] = [
        (
            in_spec.target
            if in_spec.kind
            in (
                InputKind.BUFFER,
                InputKind.CONSTANT_TENSOR,
                InputKind.PARAMETER,
                InputKind.CUSTOM_OBJ,
            )
            else None
        )
        for in_spec in ep.graph_signature.input_specs
    ]

    mutated_outputs: list[Optional[str]] = [
        (
            out_spec.target
            if out_spec.kind
            in (OutputKind.BUFFER_MUTATION, OutputKind.USER_INPUT_MUTATION)
            else None
        )
        for out_spec in ep.graph_signature.output_specs
    ]

    new_gm = _unlift(
        new_gm,
        lifted_inputs,
        mutated_outputs,
        ep.call_spec.in_spec,
        ep.call_spec.out_spec,
        ep.state_dict,
        ep.constants,
        forward_arg_names=forward_arg_names,
    )
    unlift_gm = _create_stateful_graph_module(new_gm, ep.range_constraints, ep)
    unlift_gm.meta.update(ep.graph_module.meta)
    return unlift_gm

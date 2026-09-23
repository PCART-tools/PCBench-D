def _trace_and_get_graph_from_model(model, args):

    # A basic sanity check: make sure the state_dict keys are the same
    # before and after running the model.  Fail fast!
    orig_state_dict_keys = _unique_state_dict(model).keys()

    trace_graph, torch_out, inputs_states = \
        torch.jit._get_trace_graph(model, args, strict=False, _force_outplace=False, _return_inputs_states=True)
    warn_on_static_input_change(inputs_states)

    if orig_state_dict_keys != _unique_state_dict(model).keys():
        raise RuntimeError("state_dict changed after running the tracer; "
                           "something weird is happening in your model!")

    return trace_graph, torch_out

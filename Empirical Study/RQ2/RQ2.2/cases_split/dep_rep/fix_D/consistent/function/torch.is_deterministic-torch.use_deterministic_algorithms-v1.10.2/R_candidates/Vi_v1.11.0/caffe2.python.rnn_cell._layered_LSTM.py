def _layered_LSTM(
        model, input_blob, seq_lengths, initial_states,
        dim_in, dim_out, scope, outputs_with_grads=(0,), return_params=False,
        memory_optimization=False, forget_bias=0.0, forward_only=False,
        drop_states=False, create_lstm=None):
    params = locals()  # leave it as a first line to grab all params
    params.pop('create_lstm')
    if not isinstance(dim_out, list):
        return create_lstm(**params)
    elif len(dim_out) == 1:
        params['dim_out'] = dim_out[0]
        return create_lstm(**params)

    assert len(dim_out) != 0, "dim_out list can't be empty"
    assert return_params is False, "return_params not supported for layering"
    for i, output_dim in enumerate(dim_out):
        params.update({
            'dim_out': output_dim
        })
        output, last_output, all_states, last_state = create_lstm(**params)
        params.update({
            'input_blob': output,
            'dim_in': output_dim,
            'initial_states': (last_output, last_state),
            'scope': scope + '_layer_{}'.format(i + 1)
        })
    return output, last_output, all_states, last_state

def rnn_bidirectional_layer(
    model,
    inputs,
    input_lengths,
    input_size,
    num_units,
    dropout_keep_prob,
    forward_only,
    return_sequence_output,
    return_final_state,
    scope=None,
):
    outputs_fw, final_hidden_fw, final_cell_fw = rnn_unidirectional_layer(
        model,
        inputs,
        input_lengths,
        input_size,
        num_units,
        dropout_keep_prob,
        forward_only,
        return_sequence_output,
        return_final_state,
        scope=(scope + '/' if scope else '') + 'fw',
    )
    with core.NameScope(scope):
        reversed_inputs = model.net.ReversePackedSegs(
            [inputs, input_lengths],
            ['reversed_inputs'],
        )
    outputs_bw, final_hidden_bw, final_cell_bw = rnn_unidirectional_layer(
        model,
        reversed_inputs,
        input_lengths,
        input_size,
        num_units,
        dropout_keep_prob,
        forward_only,
        return_sequence_output,
        return_final_state,
        scope=(scope + '/' if scope else '') + 'bw',
    )
    with core.NameScope(scope):
        outputs_bw = model.net.ReversePackedSegs(
            [outputs_bw, input_lengths],
            ['outputs_bw'],
        )

    # Concatenate forward and backward results
    if return_sequence_output:
        with core.NameScope(scope):
            outputs, _ = model.net.Concat(
                [outputs_fw, outputs_bw],
                ['outputs', 'outputs_dim'],
                axis=2,
            )
    else:
        outputs = None

    if return_final_state:
        with core.NameScope(scope):
            final_hidden_state, _ = model.net.Concat(
                [final_hidden_fw, final_hidden_bw],
                ['final_hidden_state', 'final_hidden_state_dim'],
                axis=2,
            )
            final_cell_state, _ = model.net.Concat(
                [final_cell_fw, final_cell_bw],
                ['final_cell_state', 'final_cell_state_dim'],
                axis=2,
            )
    else:
        final_hidden_state = None
        final_cell_state = None

    return outputs, final_hidden_state, final_cell_state

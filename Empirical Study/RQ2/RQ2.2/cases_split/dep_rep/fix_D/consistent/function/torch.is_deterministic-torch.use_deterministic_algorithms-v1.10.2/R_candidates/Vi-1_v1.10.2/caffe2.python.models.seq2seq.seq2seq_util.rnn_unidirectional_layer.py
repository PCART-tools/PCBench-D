def rnn_unidirectional_layer(
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
    """ Unidirectional LSTM encoder."""
    with core.NameScope(scope):
        initial_cell_state = model.param_init_net.ConstantFill(
            [],
            'initial_cell_state',
            shape=[num_units],
            value=0.0,
        )
        initial_hidden_state = model.param_init_net.ConstantFill(
            [],
            'initial_hidden_state',
            shape=[num_units],
            value=0.0,
        )

    cell = rnn_cell.LSTMCell(
        input_size=input_size,
        hidden_size=num_units,
        forget_bias=0.0,
        memory_optimization=False,
        name=(scope + '/' if scope else '') + 'lstm',
        forward_only=forward_only,
    )

    dropout_ratio = (
        None if dropout_keep_prob is None else (1.0 - dropout_keep_prob)
    )
    if dropout_ratio is not None:
        cell = rnn_cell.DropoutCell(
            internal_cell=cell,
            dropout_ratio=dropout_ratio,
            name=(scope + '/' if scope else '') + 'dropout',
            forward_only=forward_only,
            is_test=False,
        )

    outputs_with_grads = []
    if return_sequence_output:
        outputs_with_grads.append(0)
    if return_final_state:
        outputs_with_grads.extend([1, 3])

    outputs, (_, final_hidden_state, _, final_cell_state) = (
        cell.apply_over_sequence(
            model=model,
            inputs=inputs,
            seq_lengths=input_lengths,
            initial_states=(initial_hidden_state, initial_cell_state),
            outputs_with_grads=outputs_with_grads,
        )
    )
    return outputs, final_hidden_state, final_cell_state

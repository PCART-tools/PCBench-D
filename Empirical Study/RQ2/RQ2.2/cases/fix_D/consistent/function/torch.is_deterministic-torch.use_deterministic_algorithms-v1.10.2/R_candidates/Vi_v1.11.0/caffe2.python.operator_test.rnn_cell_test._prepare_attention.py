def _prepare_attention(t, n, dim_in, encoder_dim,
                          forward_only=False, T=None,
                          dim_out=None, residual=False,
                          final_dropout=False):
    if dim_out is None:
        dim_out = [dim_in]
    print("Dims: t={} n={} dim_in={} dim_out={}".format(t, n, dim_in, dim_out))

    model = ModelHelper(name='external')

    def generate_input_state(shape):
        return np.random.random(shape).astype(np.float32)

    initial_states = []
    for layer_id, d in enumerate(dim_out):
        h, c = model.net.AddExternalInputs(
            "hidden_init_{}".format(layer_id),
            "cell_init_{}".format(layer_id),
        )
        initial_states.extend([h, c])
        workspace.FeedBlob(h, generate_input_state((1, n, d)))
        workspace.FeedBlob(c, generate_input_state((1, n, d)))

    awec_init = model.net.AddExternalInputs([
        'initial_attention_weighted_encoder_context',
    ])
    initial_states.append(awec_init)
    workspace.FeedBlob(
        awec_init,
        generate_input_state((1, n, encoder_dim)),
    )

    # Due to convoluted RNN scoping logic we make sure that things
    # work from a namescope
    with scope.NameScope("test_name_scope"):
        (
            input_blob,
            seq_lengths,
            encoder_outputs,
            weighted_encoder_outputs,
        ) = model.net.AddScopedExternalInputs(
            'input_blob',
            'seq_lengths',
            'encoder_outputs',
            'weighted_encoder_outputs',
        )

        layer_input_dim = dim_in
        cells = []
        for layer_id, d in enumerate(dim_out):

            cell = rnn_cell.MILSTMCell(
                name='decoder_{}'.format(layer_id),
                forward_only=forward_only,
                input_size=layer_input_dim,
                hidden_size=d,
                forget_bias=0.0,
                memory_optimization=False,
            )
            cells.append(cell)
            layer_input_dim = d

        decoder_cell = rnn_cell.MultiRNNCell(
            cells,
            name='decoder',
            residual_output_layers=range(1, len(cells)) if residual else None,
        )

        attention_cell = rnn_cell.AttentionCell(
            encoder_output_dim=encoder_dim,
            encoder_outputs=encoder_outputs,
            encoder_lengths=None,
            decoder_cell=decoder_cell,
            decoder_state_dim=dim_out[-1],
            name='attention_decoder',
            attention_type=AttentionType.Recurrent,
            weighted_encoder_outputs=weighted_encoder_outputs,
            attention_memory_optimization=True,
        )
        if final_dropout:
            # dropout ratio of 0.0 used to test mechanism but not interfere
            # with numerical tests
            attention_cell = rnn_cell.DropoutCell(
                internal_cell=attention_cell,
                dropout_ratio=0.0,
                name='dropout',
                forward_only=forward_only,
                is_test=False,
            )

        attention_cell = (
            attention_cell if T is None
            else rnn_cell.UnrolledCell(attention_cell, T)
        )

        output_indices = decoder_cell.output_indices
        output_indices.append(2 * len(cells))
        outputs_with_grads = [2 * i for i in output_indices]

        final_output, state_outputs = attention_cell.apply_over_sequence(
            model=model,
            inputs=input_blob,
            seq_lengths=seq_lengths,
            initial_states=initial_states,
            outputs_with_grads=outputs_with_grads,
        )

    workspace.RunNetOnce(model.param_init_net)

    workspace.FeedBlob(
        seq_lengths,
        np.random.randint(1, t + 1, size=(n,)).astype(np.int32)
    )

    return {
        'final_output': final_output,
        'net': model.net,
        'initial_states': initial_states,
        'input_blob': input_blob,
        'encoder_outputs': encoder_outputs,
        'weighted_encoder_outputs': weighted_encoder_outputs,
        'outputs_with_grads': outputs_with_grads,
    }

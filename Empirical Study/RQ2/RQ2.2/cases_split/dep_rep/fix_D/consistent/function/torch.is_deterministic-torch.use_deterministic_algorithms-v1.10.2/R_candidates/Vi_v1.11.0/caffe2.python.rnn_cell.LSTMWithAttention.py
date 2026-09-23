def LSTMWithAttention(
    model,
    decoder_inputs,
    decoder_input_lengths,
    initial_decoder_hidden_state,
    initial_decoder_cell_state,
    initial_attention_weighted_encoder_context,
    encoder_output_dim,
    encoder_outputs,
    encoder_lengths,
    decoder_input_dim,
    decoder_state_dim,
    scope,
    attention_type=AttentionType.Regular,
    outputs_with_grads=(0, 4),
    weighted_encoder_outputs=None,
    lstm_memory_optimization=False,
    attention_memory_optimization=False,
    forget_bias=0.0,
    forward_only=False,
):
    '''
    Adds a LSTM with attention mechanism to a model.

    The implementation is based on https://arxiv.org/abs/1409.0473, with
    a small difference in the order
    how we compute new attention context and new hidden state, similarly to
    https://arxiv.org/abs/1508.04025.

    The model uses encoder-decoder naming conventions,
    where the decoder is the sequence the op is iterating over,
    while computing the attention context over the encoder.

    model: ModelHelper object new operators would be added to

    decoder_inputs: the input sequence in a format T x N x D
    where T is sequence size, N - batch size and D - input dimension

    decoder_input_lengths: blob containing sequence lengths
    which would be passed to LSTMUnit operator

    initial_decoder_hidden_state: initial hidden state of LSTM

    initial_decoder_cell_state: initial cell state of LSTM

    initial_attention_weighted_encoder_context: initial attention context

    encoder_output_dim: dimension of encoder outputs

    encoder_outputs: the sequence, on which we compute the attention context
    at every iteration

    encoder_lengths: a tensor with lengths of each encoder sequence in batch
    (may be None, meaning all encoder sequences are of same length)

    decoder_input_dim: input dimension (last dimension on decoder_inputs)

    decoder_state_dim: size of hidden states of LSTM

    attention_type: One of: AttentionType.Regular, AttentionType.Recurrent.
    Determines which type of attention mechanism to use.

    outputs_with_grads : position indices of output blobs which will receive
    external error gradient during backpropagation

    weighted_encoder_outputs: encoder outputs to be used to compute attention
    weights. In the basic case it's just linear transformation of
    encoder outputs (that the default, when weighted_encoder_outputs is None).
    However, it can be something more complicated - like a separate
    encoder network (for example, in case of convolutional encoder)

    lstm_memory_optimization: recompute LSTM activations on backward pass, so
                 we don't need to store their values in forward passes

    attention_memory_optimization: recompute attention for backward pass

    forward_only: whether to create only forward pass
    '''
    cell = LSTMWithAttentionCell(
        encoder_output_dim=encoder_output_dim,
        encoder_outputs=encoder_outputs,
        encoder_lengths=encoder_lengths,
        decoder_input_dim=decoder_input_dim,
        decoder_state_dim=decoder_state_dim,
        name=scope,
        attention_type=attention_type,
        weighted_encoder_outputs=weighted_encoder_outputs,
        forget_bias=forget_bias,
        lstm_memory_optimization=lstm_memory_optimization,
        attention_memory_optimization=attention_memory_optimization,
        forward_only=forward_only,
    )
    initial_states = [
        initial_decoder_hidden_state,
        initial_decoder_cell_state,
        initial_attention_weighted_encoder_context,
    ]
    if attention_type == AttentionType.SoftCoverage:
        initial_states.append(cell.build_initial_coverage(model))
    _, result = cell.apply_over_sequence(
        model=model,
        inputs=decoder_inputs,
        seq_lengths=decoder_input_lengths,
        initial_states=initial_states,
        outputs_with_grads=outputs_with_grads,
    )
    return result

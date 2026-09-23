def _LSTM(
    cell_class,
    model,
    input_blob,
    seq_lengths,
    initial_states,
    dim_in,
    dim_out,
    scope=None,
    outputs_with_grads=(0,),
    return_params=False,
    memory_optimization=False,
    forget_bias=0.0,
    forward_only=False,
    drop_states=False,
    return_last_layer_only=True,
    static_rnn_unroll_size=None,
    **cell_kwargs
):
    '''
    Adds a standard LSTM recurrent network operator to a model.

    cell_class: LSTMCell or compatible subclass

    model: ModelHelper object new operators would be added to

    input_blob: the input sequence in a format T x N x D
            where T is sequence size, N - batch size and D - input dimension

    seq_lengths: blob containing sequence lengths which would be passed to
            LSTMUnit operator

    initial_states: a list of (2 * num_layers) blobs representing the initial
            hidden and cell states of each layer. If this argument is None,
            these states will be added to the model as network parameters.

    dim_in: input dimension

    dim_out: number of units per LSTM layer
            (use int for single-layer LSTM, list of ints for multi-layer)

    outputs_with_grads : position indices of output blobs for LAST LAYER which
            will receive external error gradient during backpropagation.
            These outputs are: (h_all, h_last, c_all, c_last)

    return_params: if True, will return a dictionary of parameters of the LSTM

    memory_optimization: if enabled, the LSTM step is recomputed on backward
            step so that we don't need to store forward activations for each
            timestep. Saves memory with cost of computation.

    forget_bias: forget gate bias (default 0.0)

    forward_only: whether to create a backward pass

    drop_states: drop invalid states, passed through to LSTMUnit operator

    return_last_layer_only: only return outputs from final layer
            (so that length of results does depend on number of layers)

    static_rnn_unroll_size: if not None, we will use static RNN which is
    unrolled into Caffe2 graph. The size of the unroll is the value of
    this parameter.
    '''
    if type(dim_out) is not list and type(dim_out) is not tuple:
        dim_out = [dim_out]
    num_layers = len(dim_out)

    cells = []
    for i in range(num_layers):
        cell = cell_class(
            input_size=(dim_in if i == 0 else dim_out[i - 1]),
            hidden_size=dim_out[i],
            forget_bias=forget_bias,
            memory_optimization=memory_optimization,
            name=scope if num_layers == 1 else None,
            forward_only=forward_only,
            drop_states=drop_states,
            **cell_kwargs
        )
        cells.append(cell)

    cell = MultiRNNCell(
        cells,
        name=scope,
        forward_only=forward_only,
    ) if num_layers > 1 else cells[0]

    cell = (
        cell if static_rnn_unroll_size is None
        else UnrolledCell(cell, static_rnn_unroll_size))

    # outputs_with_grads argument indexes into final layer
    outputs_with_grads = [4 * (num_layers - 1) + i for i in outputs_with_grads]
    _, result = cell.apply_over_sequence(
        model=model,
        inputs=input_blob,
        seq_lengths=seq_lengths,
        initial_states=initial_states,
        outputs_with_grads=outputs_with_grads,
    )

    if return_last_layer_only:
        result = result[4 * (num_layers - 1):]
    if return_params:
        result = list(result) + [{
            'input': cell.get_input_params(),
            'recurrent': cell.get_recurrent_params(),
        }]
    return tuple(result)

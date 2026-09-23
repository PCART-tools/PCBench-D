def script_lnlstm(input_size, hidden_size, num_layers, bias=True,
                  batch_first=False, dropout=False, bidirectional=False,
                  decompose_layernorm=False):
    '''Returns a ScriptModule that mimics a PyTorch native LSTM.'''

    # The following are not implemented.
    assert bias
    assert not batch_first
    assert not dropout

    if bidirectional:
        stack_type = StackedLSTM2
        layer_type = BidirLSTMLayer
        dirs = 2
    else:
        stack_type = StackedLSTM
        layer_type = LSTMLayer
        dirs = 1

    return stack_type(num_layers, layer_type,
                      first_layer_args=[LayerNormLSTMCell, input_size, hidden_size,
                                        decompose_layernorm],
                      other_layer_args=[LayerNormLSTMCell, hidden_size * dirs,
                                        hidden_size, decompose_layernorm])

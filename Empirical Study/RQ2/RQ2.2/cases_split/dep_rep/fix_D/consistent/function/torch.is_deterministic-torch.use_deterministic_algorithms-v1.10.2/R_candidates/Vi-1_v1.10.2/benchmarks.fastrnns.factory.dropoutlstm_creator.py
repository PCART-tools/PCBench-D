def dropoutlstm_creator(script=True, **kwargs):
    assert script is True
    from .custom_lstms import script_lstm, LSTMState
    input_size = kwargs['inputSize']
    hidden_size = kwargs['hiddenSize']
    seq_len = kwargs['seqLength']
    batch_size = kwargs['miniBatch']
    num_layers = kwargs['numLayers']
    ge = script_lstm(input_size, hidden_size, num_layers, dropout=True).cuda()

    input = torch.randn(seq_len, batch_size, input_size, device='cuda')
    states = [LSTMState(torch.randn(batch_size, hidden_size, device='cuda'),
                        torch.randn(batch_size, hidden_size, device='cuda'))
              for _ in range(num_layers)]
    return ModelDef(
        inputs=[input, states],
        params=ge.parameters(),
        forward=ge,
        backward_setup=lstm_backward_setup,
        backward=simple_backward)

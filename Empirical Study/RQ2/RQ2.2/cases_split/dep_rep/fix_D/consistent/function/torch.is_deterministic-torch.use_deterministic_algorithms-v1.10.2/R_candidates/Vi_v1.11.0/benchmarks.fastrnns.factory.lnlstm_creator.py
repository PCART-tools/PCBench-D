def lnlstm_creator(script=True, decompose_layernorm=False, **kwargs):
    assert script is True
    from .custom_lstms import script_lnlstm
    input_size = kwargs['inputSize']
    hidden_size = kwargs['hiddenSize']
    seq_len = kwargs['seqLength']
    batch_size = kwargs['miniBatch']
    ge = script_lnlstm(input_size, hidden_size, 1,
                       decompose_layernorm=decompose_layernorm).cuda()

    input = torch.randn(seq_len, batch_size, input_size, device='cuda')
    states = [(torch.randn(batch_size, hidden_size, device='cuda'),
               torch.randn(batch_size, hidden_size, device='cuda'))]

    return ModelDef(
        inputs=[input, states],
        params=ge.parameters(),
        forward=ge,
        backward_setup=lstm_backward_setup,
        backward=simple_backward)

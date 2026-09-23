def layernorm_pytorch_lstm_creator(**kwargs):
    input, hidden, _, module = lstm_inputs(return_module=True, **kwargs)
    batch_size = kwargs['miniBatch']
    hidden_size = kwargs['hiddenSize']
    ln_i = torch.nn.LayerNorm(4 * hidden_size).cuda()
    ln_h = torch.nn.LayerNorm(4 * hidden_size).cuda()
    ln_c = torch.nn.LayerNorm(hidden_size).cuda()
    ln_input1 = torch.randn(batch_size, 4 * hidden_size, device='cuda')

    def forward(input, hidden):
        out, new_hidden = module(input, hidden)
        # plus (seq_len * three laynorm cell computation) to mimic the lower bound of
        # Layernorm cudnn LSTM in the forward pass
        seq_len = len(input.unbind(0))
        hy, cy = new_hidden
        for i in range(seq_len):
            ln_i_output = ln_i(ln_input1)
            ln_h_output = ln_h(ln_input1)
            cy = ln_c(cy)

        return out, (hy, cy)

    return ModelDef(
        inputs=[input, hidden],
        params=flatten_list(module.all_weights),
        forward=forward,
        backward_setup=lstm_backward_setup,
        backward=None)

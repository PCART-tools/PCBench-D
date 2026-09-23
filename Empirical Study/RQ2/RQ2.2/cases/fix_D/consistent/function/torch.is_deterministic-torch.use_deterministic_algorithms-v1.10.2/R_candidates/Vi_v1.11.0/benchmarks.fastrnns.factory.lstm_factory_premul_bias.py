def lstm_factory_premul_bias(premul_cell, script):
    def dynamic_rnn(input: Tensor, hidden: Tuple[Tensor, Tensor], wih: Tensor, whh: Tensor,
                    bih: Tensor, bhh: Tensor) -> Tuple[Tensor, Tuple[Tensor, Tensor]]:
        hx, cx = hidden
        outputs = []
        inpSize = input.size()
        # add bias for all timesteps instead of going step-by-step, results in a single reduction kernel in the backward
        # FIXME matmul(x,y) + bias currently goes through jit AD, and backward formula in AD is not optimized for this
        # case. Workaround with mm and views.
        inpSize = input.size()
        inputs = torch.mm(input.view(-1, inpSize[2]), wih.t()) + bih
        inputs = inputs.view(inpSize[0], inpSize[1], -1).unbind(0)
        hy, cy = hx[0], cx[0]
        for seq_idx in range(len(inputs)):
            hy, cy = premul_cell(inputs[seq_idx], (hy, cy), whh, bhh)
            outputs += [hy]
        return torch.stack(outputs), (hy.unsqueeze(0), cy.unsqueeze(0))

    if script:
        premul_cell = torch.jit.script(premul_cell)
        dynamic_rnn = torch.jit.script(dynamic_rnn)

    return dynamic_rnn

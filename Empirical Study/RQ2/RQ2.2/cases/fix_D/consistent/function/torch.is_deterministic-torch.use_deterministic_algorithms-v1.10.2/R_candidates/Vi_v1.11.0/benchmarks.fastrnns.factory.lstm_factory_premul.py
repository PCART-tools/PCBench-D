def lstm_factory_premul(premul_cell, script):
    def dynamic_rnn(input: Tensor, hidden: Tuple[Tensor, Tensor], wih: Tensor, whh: Tensor,
                    bih: Tensor, bhh: Tensor) -> Tuple[Tensor, Tuple[Tensor, Tensor]]:
        hx, cx = hidden
        outputs = []
        inputs = torch.matmul(input, wih.t()).unbind(0)
        hy, cy = hx[0], cx[0]
        for seq_idx in range(len(inputs)):
            hy, cy = premul_cell(inputs[seq_idx], (hy, cy), whh, bih, bhh)
            outputs += [hy]
        return torch.stack(outputs), (hy.unsqueeze(0), cy.unsqueeze(0))

    if script:
        premul_cell = torch.jit.script(premul_cell)
        dynamic_rnn = torch.jit.script(dynamic_rnn)

    return dynamic_rnn

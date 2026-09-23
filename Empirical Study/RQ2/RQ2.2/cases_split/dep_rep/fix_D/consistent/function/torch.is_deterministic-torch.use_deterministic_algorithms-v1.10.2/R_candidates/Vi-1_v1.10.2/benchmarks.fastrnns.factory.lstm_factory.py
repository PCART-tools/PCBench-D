def lstm_factory(cell, script):
    def dynamic_rnn(input: Tensor, hidden: Tuple[Tensor, Tensor], wih: Tensor, whh: Tensor,
                    bih: Tensor, bhh: Tensor) -> Tuple[Tensor, Tuple[Tensor, Tensor]]:
        hx, cx = hidden
        outputs = []
        inputs = input.unbind(0)
        hy, cy = hx[0], cx[0]
        for seq_idx in range(len(inputs)):
            hy, cy = cell(inputs[seq_idx], (hy, cy), wih, whh, bih, bhh)
            outputs += [hy]
        return torch.stack(outputs), (hy.unsqueeze(0), cy.unsqueeze(0))

    if script:
        cell = torch.jit.script(cell)
        dynamic_rnn = torch.jit.script(dynamic_rnn)

    return dynamic_rnn

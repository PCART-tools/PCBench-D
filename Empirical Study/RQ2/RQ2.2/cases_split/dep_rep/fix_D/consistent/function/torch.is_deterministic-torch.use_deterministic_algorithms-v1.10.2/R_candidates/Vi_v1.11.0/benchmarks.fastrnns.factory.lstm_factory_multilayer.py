def lstm_factory_multilayer(cell, script):
    def dynamic_rnn(input: Tensor, hidden: Tuple[Tensor, Tensor], params: List[Tensor]) -> Tuple[Tensor, Tuple[Tensor, Tensor]]:
        params_stride = 4  # NB: this assumes that biases are there
        hx, cx = hidden
        hy, cy = hidden  # for scoping...
        inputs, outputs = input.unbind(0), []
        for layer in range(hx.size(0)):
            hy = hx[layer]
            cy = cx[layer]
            base_idx = layer * params_stride
            wih = params[base_idx]
            whh = params[base_idx + 1]
            bih = params[base_idx + 2]
            bhh = params[base_idx + 3]
            for seq_idx in range(len(inputs)):
                hy, cy = cell(inputs[seq_idx], (hy, cy), wih, whh, bih, bhh)
                outputs += [hy]
            inputs, outputs = outputs, []
        return torch.stack(inputs), (hy.unsqueeze(0), cy.unsqueeze(0))

    if script:
        cell = torch.jit.script(cell)
        dynamic_rnn = torch.jit.script(dynamic_rnn)

    return dynamic_rnn

def varlen_lstm_factory(cell, script):
    def dynamic_rnn(sequences: List[Tensor], hiddens: Tuple[Tensor, Tensor], wih: Tensor,
                    whh: Tensor, bih: Tensor, bhh: Tensor
                    ) -> Tuple[List[Tensor], Tuple[List[Tensor], List[Tensor]]]:
        hx, cx = hiddens
        hxs = hx.unbind(1)
        cxs = cx.unbind(1)
        # List of: (output, hx, cx)
        outputs = []
        hx_outs = []
        cx_outs = []

        for batch in range(len(sequences)):
            output = []
            hy, cy = hxs[batch], cxs[batch]
            inputs = sequences[batch].unbind(0)

            for seq_idx in range(len(inputs)):
                hy, cy = cell(
                    inputs[seq_idx].unsqueeze(0), (hy, cy), wih, whh, bih, bhh)
                output += [hy]
            outputs += [torch.stack(output)]
            hx_outs += [hy.unsqueeze(0)]
            cx_outs += [cy.unsqueeze(0)]

        return outputs, (hx_outs, cx_outs)

    if script:
        cell = torch.jit.script(cell)
        dynamic_rnn = torch.jit.script(dynamic_rnn)

    return dynamic_rnn

def flat_lstm_cell(input: Tensor, hx: Tensor, cx: Tensor, w_ih: Tensor,
                   w_hh: Tensor, b_ih: Tensor, b_hh: Tensor) -> Tuple[Tensor, Tensor]:
    gates = torch.mm(input, w_ih.t()) + torch.mm(hx, w_hh.t()) + b_ih + b_hh

    ingate, forgetgate, cellgate, outgate = gates.chunk(4, 1)

    ingate = torch.sigmoid(ingate)
    forgetgate = torch.sigmoid(forgetgate)
    cellgate = torch.tanh(cellgate)
    outgate = torch.sigmoid(outgate)

    cy = (forgetgate * cx) + (ingate * cellgate)
    hy = outgate * torch.tanh(cy)

    return hy, cy

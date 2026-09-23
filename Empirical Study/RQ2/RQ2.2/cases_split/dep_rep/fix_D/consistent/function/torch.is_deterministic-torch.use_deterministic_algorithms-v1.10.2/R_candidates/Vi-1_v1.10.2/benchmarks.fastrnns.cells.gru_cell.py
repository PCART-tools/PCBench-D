def gru_cell(input, hidden, w_ih, w_hh, b_ih, b_hh):
    gi = torch.mm(input, w_ih.t()) + b_ih
    gh = torch.mm(hidden, w_hh.t()) + b_hh
    i_r, i_i, i_n = gi.chunk(3, 1)
    h_r, h_i, h_n = gh.chunk(3, 1)

    resetgate = torch.sigmoid(i_r + h_r)
    inputgate = torch.sigmoid(i_i + h_i)
    newgate = torch.tanh(i_n + resetgate * h_n)
    hy = newgate + inputgate * (hidden - newgate)

    return hy

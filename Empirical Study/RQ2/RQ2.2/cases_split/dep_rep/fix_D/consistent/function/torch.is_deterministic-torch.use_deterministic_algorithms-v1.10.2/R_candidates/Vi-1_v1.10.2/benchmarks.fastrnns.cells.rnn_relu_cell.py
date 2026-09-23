def rnn_relu_cell(input, hidden, w_ih, w_hh, b_ih, b_hh):
    igates = torch.mm(input, w_ih.t()) + b_ih
    hgates = torch.mm(hidden, w_hh.t()) + b_hh
    return torch.relu(igates + hgates)

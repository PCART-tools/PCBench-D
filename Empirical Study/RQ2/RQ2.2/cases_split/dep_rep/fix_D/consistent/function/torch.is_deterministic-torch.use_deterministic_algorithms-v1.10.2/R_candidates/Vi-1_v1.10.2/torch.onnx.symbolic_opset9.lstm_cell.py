def lstm_cell(g, self, hidden, w_ih, w_hh, b_ih, b_hh):
    input = sym_help._unsqueeze_helper(g, self, [0])
    hidden = sym_help._unpack_list(hidden)
    hidden = [sym_help._unsqueeze_helper(g, x, [0]) for x in hidden]
    weight = (w_ih, w_hh, b_ih, b_hh) if sym_help._is_tensor(b_ih) else (w_ih, w_hh)
    has_biases = True if sym_help._is_tensor(b_ih) else False
    _, h_outs, c_outs = _generic_rnn(g, 'LSTM', input, hidden, weight, has_biases, num_layers=1,
                                     dropout=0, train=0, bidirectional=False, batch_first=False)
    return sym_help._squeeze_helper(g, h_outs, [0]), sym_help._squeeze_helper(g, c_outs, [0])

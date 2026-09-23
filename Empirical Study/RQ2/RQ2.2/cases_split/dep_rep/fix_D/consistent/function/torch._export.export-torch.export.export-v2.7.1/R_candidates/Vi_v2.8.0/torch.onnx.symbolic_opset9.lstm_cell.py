@_onnx_symbolic("aten::lstm_cell")
def lstm_cell(g: jit_utils.GraphContext, self, hidden, w_ih, w_hh, b_ih, b_hh):
    input = symbolic_helper._unsqueeze_helper(g, self, [0])
    hidden = symbolic_helper._unpack_list(hidden)
    hidden = [symbolic_helper._unsqueeze_helper(g, x, [0]) for x in hidden]
    weight = (
        (w_ih, w_hh, b_ih, b_hh) if symbolic_helper._is_tensor(b_ih) else (w_ih, w_hh)
    )
    has_biases = True if symbolic_helper._is_tensor(b_ih) else False
    _, h_outs, c_outs = _generic_rnn(
        g,
        "LSTM",
        input,
        hidden,
        weight,
        has_biases,
        num_layers=1,
        dropout=0,
        train=0,
        bidirectional=False,
        batch_first=False,
    )
    return symbolic_helper._squeeze_helper(
        g, h_outs, [0]
    ), symbolic_helper._squeeze_helper(g, c_outs, [0])

@parse_args("v", "v", "v", "v", "i", "i", "f", "i", "i")
def _lstm_packed(g, input, batch_sizes, hidden_v, weight_v, has_biases, num_layers, dropout, train, bidirectional):
    hidden, weight = sym_help._unpack_list(hidden_v), sym_help._unpack_list(weight_v)
    return _generic_rnn(g, "LSTM", input, hidden, weight, has_biases, num_layers,
                        dropout, train, bidirectional, batch_sizes=batch_sizes)

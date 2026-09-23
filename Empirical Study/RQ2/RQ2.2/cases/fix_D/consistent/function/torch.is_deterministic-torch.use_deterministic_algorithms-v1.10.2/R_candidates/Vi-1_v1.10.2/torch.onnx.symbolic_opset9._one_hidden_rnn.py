def _one_hidden_rnn(kind):
    @parse_args("v", "v", "v", "i", "i", "f", "i", "i", "i")
    def _rnn_full(g, input, hidden, weight_v, has_biases, num_layers, dropout, train, bidirectional, batch_first):
        weight = sym_help._unpack_list(weight_v)
        return _generic_rnn(g, kind, input, hidden, weight, has_biases, num_layers,
                            dropout, train, bidirectional, batch_first)

    @parse_args("v", "v", "v", "v", "i", "i", "f", "i", "i")
    def _rnn_packed(g, input, batch_sizes, hidden, weight_v, has_biases, num_layers, dropout, train, bidirectional):
        weight = sym_help._unpack_list(weight_v)
        return _generic_rnn(g, kind, input, hidden, weight, has_biases, num_layers,
                            dropout, train, bidirectional, batch_sizes=batch_sizes)

    def symbolic(g, *args):
        if sym_help._is_tensor_list(args[3]):
            return _rnn_packed(g, *args)
        else:
            return _rnn_full(g, *args)

    return symbolic

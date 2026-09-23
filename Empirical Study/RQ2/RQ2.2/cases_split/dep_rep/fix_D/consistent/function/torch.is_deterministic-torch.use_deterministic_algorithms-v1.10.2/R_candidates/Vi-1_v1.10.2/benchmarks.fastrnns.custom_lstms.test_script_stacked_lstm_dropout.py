def test_script_stacked_lstm_dropout(seq_len, batch, input_size, hidden_size,
                                     num_layers):
    inp = torch.randn(seq_len, batch, input_size)
    states = [LSTMState(torch.randn(batch, hidden_size),
                        torch.randn(batch, hidden_size))
              for _ in range(num_layers)]
    rnn = script_lstm(input_size, hidden_size, num_layers, dropout=True)

    # just a smoke test
    out, out_state = rnn(inp, states)

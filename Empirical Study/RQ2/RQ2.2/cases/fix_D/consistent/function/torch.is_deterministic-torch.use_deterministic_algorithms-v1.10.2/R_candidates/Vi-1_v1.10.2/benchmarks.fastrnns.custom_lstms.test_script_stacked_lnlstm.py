def test_script_stacked_lnlstm(seq_len, batch, input_size, hidden_size,
                               num_layers):
    inp = torch.randn(seq_len, batch, input_size)
    states = [LSTMState(torch.randn(batch, hidden_size),
                        torch.randn(batch, hidden_size))
              for _ in range(num_layers)]
    rnn = script_lnlstm(input_size, hidden_size, num_layers)

    # just a smoke test
    out, out_state = rnn(inp, states)

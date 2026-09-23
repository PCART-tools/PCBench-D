def varlen_lstm_backward_setup(forward_output, seed=None):
    if seed:
        torch.manual_seed(seed)
    rnn_utils = torch.nn.utils.rnn
    sequences = forward_output[0]
    padded = rnn_utils.pad_sequence(sequences)
    grad = torch.randn_like(padded)
    return padded, grad

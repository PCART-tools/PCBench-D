def varlen_lstm_inputs(minlen=30, maxlen=100,
                       numLayers=1, inputSize=512, hiddenSize=512,
                       miniBatch=64, return_module=False, device='cuda',
                       seed=None, **kwargs):
    if seed is not None:
        torch.manual_seed(seed)
    lengths = torch.randint(
        low=minlen, high=maxlen, size=[miniBatch],
        dtype=torch.long, device=device)
    x = [torch.randn(length, inputSize, device=device)
         for length in lengths]
    hx = torch.randn(numLayers, miniBatch, hiddenSize, device=device)
    cx = torch.randn(numLayers, miniBatch, hiddenSize, device=device)
    lstm = torch.nn.LSTM(inputSize, hiddenSize, numLayers).to(device)

    if return_module:
        return x, lengths, (hx, cx), lstm.all_weights, lstm
    else:
        # NB: lstm.all_weights format:
        # wih, whh, bih, bhh = lstm.all_weights[layer]
        return x, lengths, (hx, cx), lstm.all_weights, None

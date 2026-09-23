def get_deepspeech(device: torch.device) -> GetterReturnType:
    sample_rate = 16000
    window_size = 0.02
    window = "hamming"
    audio_conf = dict(sample_rate=sample_rate,
                      window_size=window_size,
                      window=window,
                      noise_dir=None)

    N = 10
    num_classes = 10
    spectrogram_size = 161
    # Commented are the original sizes in the code
    seq_length = 500  # 1343
    target_length = 10  # 50
    labels = torch.rand(num_classes, device=device)
    inputs = torch.rand(N, 1, spectrogram_size, seq_length, device=device)
    # Sequence length for each input
    inputs_sizes = torch.rand(N, device=device).mul(seq_length * 0.1).add(seq_length * 0.8)
    targets = torch.rand(N, target_length, device=device)
    targets_sizes = torch.full((N,), target_length, dtype=torch.int, device=device)

    model = models.DeepSpeech(rnn_type=nn.LSTM, labels=labels, rnn_hidden_size=1024, nb_layers=5,
                              audio_conf=audio_conf, bidirectional=True)
    model = model.to(device)
    criterion = nn.CTCLoss()
    params, names = extract_weights(model)

    def forward(*new_params: Tensor) -> Tensor:
        load_weights(model, names, new_params)
        out, out_sizes = model(inputs, inputs_sizes)
        out = out.transpose(0, 1)  # For ctc loss

        loss = criterion(out, targets, out_sizes, targets_sizes)
        return loss

    return forward, params

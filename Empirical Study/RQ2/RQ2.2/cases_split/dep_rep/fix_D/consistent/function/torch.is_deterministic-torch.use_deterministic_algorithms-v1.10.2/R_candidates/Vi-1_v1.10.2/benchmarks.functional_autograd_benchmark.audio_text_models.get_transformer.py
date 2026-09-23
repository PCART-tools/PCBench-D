def get_transformer(device: torch.device) -> GetterReturnType:
    # For most SOTA research, you would like to have embed to 720, nhead to 12, bsz to 64, tgt_len/src_len to 128.
    N = 64
    seq_length = 128
    ntoken = 50
    model = models.TransformerModel(ntoken=ntoken, ninp=720, nhead=12, nhid=2048, nlayers=2)
    model.to(device)
    criterion = nn.NLLLoss()
    params, names = extract_weights(model)

    data = torch.rand(N, seq_length + 1, device=device).mul(ntoken).long()
    inputs = data.narrow(1, 0, seq_length)
    targets = data.narrow(1, 1, seq_length)

    def forward(*new_params: Tensor) -> Tensor:
        load_weights(model, names, new_params)
        out = model(inputs)

        loss = criterion(out.reshape(N * seq_length, ntoken), targets.reshape(N * seq_length))
        return loss

    return forward, params

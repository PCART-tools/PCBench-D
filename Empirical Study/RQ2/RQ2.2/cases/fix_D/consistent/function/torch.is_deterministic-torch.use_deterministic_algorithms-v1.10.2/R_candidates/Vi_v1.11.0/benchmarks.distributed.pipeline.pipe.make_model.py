def make_model(args, device, ntokens):
    ninp = 2048  # embedding dimension
    nhid = 2048  # the dimension of the feedforward network model in nn.TransformerEncoder
    nhead = 32  # the number of heads in the multiheadattention models
    dropout = 0
    initrange = 0.1
    ndecoder = args.num_decoder_layers

    model = TransformerLMSequential(ntokens, ninp, nhead, nhid, dropout, initrange, ndecoder).to(device)

    criterion = nn.CrossEntropyLoss()
    lr = 0.01  # learning rate

    def make_adam(model):
        return Adam(model.parameters(), lr=lr)

    optimizer = make_adam

    return model, criterion, optimizer

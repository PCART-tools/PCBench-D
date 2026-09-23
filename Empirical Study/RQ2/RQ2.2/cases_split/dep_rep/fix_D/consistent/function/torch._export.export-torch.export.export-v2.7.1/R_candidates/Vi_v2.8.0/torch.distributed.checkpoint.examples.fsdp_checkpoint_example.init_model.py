def init_model():
    model = FSDP(torch.nn.Linear(4, 4).cuda(dist.get_rank()))
    optim = torch.optim.Adam(model.parameters(), lr=0.1)
    model(torch.rand(4, 4)).sum().backward()
    optim.step()

    return model, optim

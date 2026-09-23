def weight_init(module):
    if isinstance(module, torch.nn.Linear):
        stdev = 1.0 / math.sqrt(module.weight.size(1))
        for p in module.parameters():
            p.data.uniform_(-stdev, stdev)

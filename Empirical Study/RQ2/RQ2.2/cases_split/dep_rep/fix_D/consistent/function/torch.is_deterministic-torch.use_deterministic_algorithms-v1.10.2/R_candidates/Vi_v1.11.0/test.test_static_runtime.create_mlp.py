def create_mlp(ln, sigmoid_layer):
    layers = nn.ModuleList()
    for i in range(0, len(ln) - 1):
        n = ln[i]
        m = ln[i + 1]

        LL = nn.Linear(int(n), int(m), bias=True)

        mean = 0.0  # std_dev = np.sqrt(variance)
        std_dev = np.sqrt(2 / (m + n))  # np.sqrt(1 / m) # np.sqrt(1 / n)
        W = np.random.normal(mean, std_dev, size=(m, n)).astype(np.float32)
        std_dev = np.sqrt(1 / m)  # np.sqrt(2 / (m + 1))
        bt = np.random.normal(mean, std_dev, size=m).astype(np.float32)
        LL.weight.data = torch.tensor(W, requires_grad=True)
        LL.bias.data = torch.tensor(bt, requires_grad=True)
        layers.append(LL)

        if i == sigmoid_layer:
            layers.append(nn.Sigmoid())
        else:
            layers.append(nn.ReLU())

    with torch.no_grad():
        s = torch.jit.script(torch.nn.Sequential(*layers))
    s.eval()
    return s

def run(initializer):
    torch.manual_seed(0)

    layer1 = torch.nn.Linear(7, 15)
    INITIALIZERS[initializer](layer1.weight)

    layer2 = torch.nn.Linear(15, 15)
    INITIALIZERS[initializer](layer2.weight)

    layer3 = torch.nn.Linear(15, 2)
    INITIALIZERS[initializer](layer3.weight)

    weight1 = layer1.weight.data.numpy()
    weight2 = layer2.weight.data.numpy()
    weight3 = layer3.weight.data.numpy()

    return [weight1, weight2, weight3]

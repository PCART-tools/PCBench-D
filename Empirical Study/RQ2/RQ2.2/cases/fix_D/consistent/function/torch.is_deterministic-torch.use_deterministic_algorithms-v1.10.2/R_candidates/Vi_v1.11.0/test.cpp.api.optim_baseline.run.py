def run(optimizer_name, iterations, sample_every):
    torch.manual_seed(0)
    model = torch.nn.Sequential(
        torch.nn.Linear(2, 3),
        torch.nn.Sigmoid(),
        torch.nn.Linear(3, 1),
        torch.nn.Sigmoid(),
    )
    model = model.to(torch.float64).apply(weight_init)

    optimizer = OPTIMIZERS[optimizer_name](model.parameters())

    input = torch.tensor([[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]], dtype=torch.float64)

    values = []
    for i in range(iterations):
        optimizer.zero_grad()

        output = model.forward(input)
        loss = output.sum()
        loss.backward()

        def closure():
            return torch.tensor([10.])
        optimizer.step(closure)

        if i % sample_every == 0:

            values.append(
                [p.clone().flatten().data.numpy() for p in model.parameters()]
            )

    return values

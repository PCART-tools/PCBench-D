def get_resnet18(device: torch.device) -> GetterReturnType:
    N = 32
    model = models.resnet18(pretrained=False)
    criterion = torch.nn.CrossEntropyLoss()
    model.to(device)
    params, names = extract_weights(model)

    inputs = torch.rand([N, 3, 224, 224], device=device)
    labels = torch.rand(N, device=device).mul(10).long()

    def forward(*new_params: Tensor) -> Tensor:
        load_weights(model, names, new_params)
        out = model(inputs)

        loss = criterion(out, labels)
        return loss

    return forward, params

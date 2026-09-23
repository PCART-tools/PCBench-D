def get_fcn_resnet(device: torch.device) -> GetterReturnType:
    N = 8
    criterion = torch.nn.MSELoss()
    model = models.fcn_resnet50(pretrained=False, pretrained_backbone=False)
    model.to(device)
    params, names = extract_weights(model)

    inputs = torch.rand([N, 3, 480, 480], device=device)
    # Given model has 21 classes
    labels = torch.rand([N, 21, 480, 480], device=device)

    def forward(*new_params: Tensor) -> Tensor:
        load_weights(model, names, new_params)
        out = model(inputs)['out']

        loss = criterion(out, labels)
        return loss

    return forward, params

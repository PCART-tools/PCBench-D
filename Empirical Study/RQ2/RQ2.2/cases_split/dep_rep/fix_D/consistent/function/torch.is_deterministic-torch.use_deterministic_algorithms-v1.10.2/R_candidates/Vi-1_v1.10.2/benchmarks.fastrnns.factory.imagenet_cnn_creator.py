def imagenet_cnn_creator(arch, jit=True):
    def creator(device='cuda', **kwargs):
        model = arch().to(device)
        x = torch.randn(32, 3, 224, 224, device=device)
        if jit:
            model = torch.jit.trace(model, x)
        return ModelDef(
            inputs=(x,),
            params=list(model.parameters()),
            forward=model,
            backward_setup=simple_backward_setup,
            backward=simple_backward)

    return creator

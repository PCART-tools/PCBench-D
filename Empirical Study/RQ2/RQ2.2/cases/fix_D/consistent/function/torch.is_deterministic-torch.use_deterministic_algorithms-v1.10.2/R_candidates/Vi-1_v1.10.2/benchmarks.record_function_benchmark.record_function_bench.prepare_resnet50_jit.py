def prepare_resnet50_jit(bench_args):
    model = resnet50()
    inputs = (torch.randn(32, 3, 224, 224),)
    model = torch.jit.trace(model, inputs)
    return inputs, model

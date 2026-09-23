def cast_to_fp64(model, inputs):
    return cast_to(torch.float64, model, inputs)

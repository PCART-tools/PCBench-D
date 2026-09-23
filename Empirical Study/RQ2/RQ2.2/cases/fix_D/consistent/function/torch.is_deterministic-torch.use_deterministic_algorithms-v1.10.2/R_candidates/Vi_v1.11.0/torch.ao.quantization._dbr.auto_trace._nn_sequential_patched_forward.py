def _nn_sequential_patched_forward(cls, input):
    for module in cls:
        if not isinstance(module, AutoQuantizationState):
            input = module(input)
    return input

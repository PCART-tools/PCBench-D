def is_activation_post_process(module):
    return (isinstance(module, torch.quantization.ObserverBase) or
            isinstance(module, torch.quantization.FakeQuantizeBase))

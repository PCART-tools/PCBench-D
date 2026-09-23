def is_activation_post_process(module):
    return (isinstance(module, torch.ao.quantization.ObserverBase) or
            isinstance(module, torch.ao.quantization.FakeQuantizeBase))

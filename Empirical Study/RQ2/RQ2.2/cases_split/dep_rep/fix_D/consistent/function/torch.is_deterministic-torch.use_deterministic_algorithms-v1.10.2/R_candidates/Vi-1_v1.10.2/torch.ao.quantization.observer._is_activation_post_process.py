def _is_activation_post_process(module):
    return (
        isinstance(module, torch.quantization.ObserverBase)
        or isinstance(module, torch.quantization.FakeQuantize)
        or _is_observer_script_module(module, "quantization.observer")
    )

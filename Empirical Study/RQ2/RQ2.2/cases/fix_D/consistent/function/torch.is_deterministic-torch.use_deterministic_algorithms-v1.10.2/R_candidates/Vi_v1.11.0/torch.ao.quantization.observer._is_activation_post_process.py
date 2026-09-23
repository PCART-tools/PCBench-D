def _is_activation_post_process(module):
    return (
        isinstance(module, torch.ao.quantization.ObserverBase)
        or isinstance(module, torch.ao.quantization.FakeQuantize)
        or _is_observer_script_module(module, "quantization.observer")
    )

def register_activation_post_process_hook(module, pre_hook=False):
    assert hasattr(module, 'activation_post_process'), \
        'Expect activation_post_process attribute already attached to the module'
    if pre_hook:
        handle = module.register_forward_pre_hook(_observer_forward_pre_hook)
        module._forward_pre_hooks.move_to_end(handle.id, last=False)
    else:
        handle = module.register_forward_hook(_observer_forward_hook)
        module._forward_hooks.move_to_end(handle.id, last=False)

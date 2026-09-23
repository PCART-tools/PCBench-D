def register_activation_post_process_hook(module):
    assert hasattr(module, 'activation_post_process'), \
        'Expect activation_post_process attribut already attached to the module'
    return module.register_forward_hook(_observer_forward_hook)

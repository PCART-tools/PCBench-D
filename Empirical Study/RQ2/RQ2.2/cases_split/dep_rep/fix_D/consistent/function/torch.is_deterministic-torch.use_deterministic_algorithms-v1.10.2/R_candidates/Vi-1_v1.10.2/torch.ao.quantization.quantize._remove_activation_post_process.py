def _remove_activation_post_process(module):
    # TODO: maybe we should change activation_post_process to _activation_post_process
    # to prevent it from being used by user
    if hasattr(module, 'activation_post_process') and \
       is_activation_post_process(module.activation_post_process):
        delattr(module, 'activation_post_process')

    # remove activation_post_proceess hook
    handle_ids_to_remove = set()
    for handle_id, hook_fn in module._forward_hooks.items():
        if hook_fn is _observer_forward_hook:
            handle_ids_to_remove.add(handle_id)
    for handle_id in handle_ids_to_remove:
        module._forward_hooks.pop(handle_id)

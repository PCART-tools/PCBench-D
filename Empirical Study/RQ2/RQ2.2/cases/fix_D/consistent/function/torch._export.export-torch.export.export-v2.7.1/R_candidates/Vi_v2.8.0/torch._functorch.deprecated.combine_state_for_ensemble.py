def combine_state_for_ensemble(models):
    warn_deprecated("combine_state_for_ensemble", "torch.func.stack_module_state")
    return _nn_impl.combine_state_for_ensemble(models)

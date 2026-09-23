def disable_if_config_true(func):
    @functools.wraps(func)
    def fsdp_hook_wrapper(*args, **kwargs):
        if torch._dynamo.config.skip_fsdp_hooks:
            return torch._dynamo.disable(func, recursive=True)(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return fsdp_hook_wrapper

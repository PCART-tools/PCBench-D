@functools.lru_cache
def dill_available() -> bool:
    return (
        _check_module_exists("dill")
        # dill fails to import under torchdeploy
        and not torch._running_with_deploy()
    )

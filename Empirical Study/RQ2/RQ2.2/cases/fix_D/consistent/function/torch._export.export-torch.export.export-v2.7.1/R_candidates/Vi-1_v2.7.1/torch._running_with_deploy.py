def _running_with_deploy() -> builtins.bool:
    return sys.modules.get("torch._meta_registrations", None) is object

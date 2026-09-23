def find_torch_dispatch_rule(op, torch_dispatch_class: type) -> Optional[Callable]:
    return singleton.find(op.__qualname__).torch_dispatch_rules.find(
        torch_dispatch_class
    )

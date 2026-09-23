def is_symbolic(a: Any) -> TypeGuard[Union[torch.SymInt, torch.Tensor]]:
    return isinstance(a, torch.SymInt) or (
        isinstance(a, torch.Tensor)
        and any(is_symbolic(x) for x in itertools.chain(a.size(), a.stride()))
    )

def _change_class(module) -> None:
    cls = module.__class__
    func_params : Dict[str, Tensor] = module._functional_parameters

    def _getattribute(self, name: str) -> Any:
        if name in func_params:
            return func_params[name]
        return cls.__getattribute__(self, name)

    param_cls = type(
        f"StatelessReplacer{cls.__name__}",
        (cls,),
        {
            "__getattribute__": _getattribute,
        },
    )

    module.__class__ = param_cls
    module._orig_class = cls

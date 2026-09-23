def _inject_new_class(module: Module) -> None:
    r"""Sets up a module to be parametrized.

    This works by substituting the class of the module by a class
    that extends it to be able to inject a property

    Args:
        module (nn.Module): module into which to inject the property
    """
    cls = module.__class__

    def getstate(self):
        raise RuntimeError(
            "Serialization of parametrized modules is only "
            "supported through state_dict(). See:\n"
            "https://pytorch.org/tutorials/beginner/saving_loading_models.html"
            "#saving-loading-a-general-checkpoint-for-inference-and-or-resuming-training"
        )

    param_cls = type(
        f"Parametrized{cls.__name__}",
        (cls,),
        {
            "__getstate__": getstate,
        },
    )

    module.__class__ = param_cls

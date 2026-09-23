def _rewrite(mod_to_rewrite: nn.Module, allow_list: Optional[Set] = None) -> nn.Module:
    if allow_list is None:
        allow_list = DEFAULT_REWRITE_ALLOW_LIST
    else:
        allow_list.union(DEFAULT_REWRITE_ALLOW_LIST)

    # Rewrite this module's functions as well as all recursive modules'
    # functions that are attrs of this moodule. Return the new, rewritten module
    # hierarchy.
    def rewrite_module(m: nn.Module):
        base_class : Type[nn.Module] = type(m)

        # Keep track of all the ConditionalExceptionWrappers that the
        # Acc_Rewriter calls into in this module so we can add them in init
        # below.
        all_added_wrappers: Set[Type[Exception]] = set()

        # Note: Make this a subclass of our base class.
        class RewrittenModule(base_class):  # type: ignore[valid-type, misc]
            # Keep track of the base_class so that symbolic tracing can
            # determine what kind of module this originally was later on.
            _base_class_origin = base_class
            # Add suffix to qualname so it's easier to debug the origin of this module.
            __qualname__ = f"{base_class.__qualname__}__AccRewrittenModule"

            # Write all of the non-dunder or special methods from base_class
            # into RewrittenModule.
            for method_name in dir(base_class):
                method = getattr(base_class, method_name)
                if builtins.type(method) is not FunctionType:
                    continue

                # Always skip rewriting dunder methods, as they haven't (yet) been
                # problematic, and modifying them has caused issues previously.
                if method_name.startswith("__") and method_name.endswith("__"):
                    continue

                # Only rewrite those Modules explicitly in the allow_list.
                assert allow_list is not None
                if base_class not in allow_list:
                    vars()[method_name] = method
                else:
                    vars()[method_name], added_wrappers = Acc_Rewriter().rewrite(method)
                    all_added_wrappers.update(added_wrappers)

            def __init__(self, orig):
                nn.Module.__init__(self)
                # Iterate over all added exception wrappers and add
                # ConditionalExceptionWrapper attrs for each.
                for exc_type in all_added_wrappers:
                    wrapper_name = _get_exception_wrapper_attr_name(exc_type)
                    assert not hasattr(self, wrapper_name)
                    setattr(
                        self,
                        wrapper_name,
                        ConditionalExceptionWrapper(exc_type),
                    )
                # Recursively rewrite and copy all module attrs of this module.
                for k, v in orig.__dict__.items():
                    if k == "_modules":
                        for mod_k, mod_v in v.items():
                            self._modules[mod_k] = rewrite_module(mod_v)
                    else:
                        self.__dict__[k] = v

        # Add suffix to name so it's easier to debug the origin of this module.
        RewrittenModule.__name__ = f"{base_class.__name__}__AccRewrittenModule"
        return RewrittenModule(m)

    return rewrite_module(mod_to_rewrite)

@contextmanager
def _detect_attribute_assignment(mod: torch.nn.Module):
    # Do not allow assignment of tensor attributes during export unless
    # the attribute is registered as a buffer.

    NN_MODULE_STD_ATTRS = [
        "_backward_hooks",
        "_backward_pre_hooks",
        "_buffers",
        "_forward_hooks",
        "_forward_hooks_always_called",
        "_forward_hooks_with_kwargs",
        "_forward_pre_hooks",
        "_forward_pre_hooks_with_kwargs",
        "_is_full_backward_hook",
        "_load_state_dict_post_hooks",
        "_load_state_dict_pre_hooks",
        "_modules",
        "_non_persistent_buffers_set",
        "_parameters",
        "_state_dict_hooks",
        "_state_dict_pre_hooks",
        "training",
    ]
    NN_MODULE_LAZY_STD_ATTRS = [
        "_initialize_hook",
        "_load_hook",
    ]
    STD_ATTRS = {
        *NN_MODULE_STD_ATTRS,
        *NN_MODULE_LAZY_STD_ATTRS,
    }

    def _get_attributes(mod):
        # return any attributes of a module that are not standard attributes
        return {k: v for k, v in mod.__dict__.items() if k not in STD_ATTRS}

    def is_leaf(x):
        # Ideally is_leaf should not be needed when mapping, but it seems that
        # subclasses of a standard container X may sometimes map to X, which
        # destroys information and can cause future mapping to fail.
        known_subclasses_that_lose_info = (
            torch.Size,
            # add more here if needed
        )
        return isinstance(x, known_subclasses_that_lose_info)

    # save state of attributes before enter
    snapshot = pytree.tree_map(lambda x: x, _get_attributes(mod), is_leaf=is_leaf)
    try:
        yield
    finally:
        # after exit, compare state of attributes with snapshot
        # to detect which tensor attributes were assigned
        assigned_tensor_attributes = []

        def _collect_assigned_tensor_attributes(kp, v, _v):
            if _v is not v:
                attr, *rest = kp
                if isinstance(v, torch.Tensor):
                    assigned_tensor_attributes.append(
                        f"self.{attr.key}{pytree.keystr(rest)}"
                    )
                # TODO(avik): Assigning all other types are allowed right now.
                # Maybe in the future we want to limit this to primitive types?

        pytree.tree_map_with_path(
            _collect_assigned_tensor_attributes, snapshot, _get_attributes(mod)
        )
        # restore state of all attributes (including, e.g., of primitive types)
        mod.__dict__.update(snapshot)

        if assigned_tensor_attributes:
            if len(assigned_tensor_attributes) > 1:
                noun, verb = "attributes", "were"
            else:
                noun, verb = "attribute", "was"
            raise ValueError(
                f"The tensor {noun} {', '.join(assigned_tensor_attributes)} {verb} assigned during export. "
                "Such attributes must be registered as buffers using the `register_buffer` API "
                "(https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.register_buffer)."
            )

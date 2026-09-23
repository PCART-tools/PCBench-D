def was_tensor_metadata_updated(arg, new_arg):
    if is_traceable_wrapper_subclass(arg):
        assert is_traceable_wrapper_subclass(new_arg)
        attrs, _ = arg.__tensor_flatten__()
        new_attrs, _ = new_arg.__tensor_flatten__()
        assert attrs == new_attrs
        # A tensor subclass was updated if any of its inner elements were updated
        return any(
            was_tensor_metadata_updated(getattr(arg, attr), getattr(new_arg, attr))
            for attr in attrs
        )
    else:
        return arg is not new_arg and StorageWeakRef(
            arg.untyped_storage()
        ) == StorageWeakRef(new_arg.untyped_storage())

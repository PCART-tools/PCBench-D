def _validate_nestedness(query: Tensor, key: Tensor, value: Tensor):
    # Currently, inputs can only be all nested or no nested.
    if query.is_nested != key.is_nested or key.is_nested != value.is_nested:
        raise ValueError(
            "FlexAttention does not support mixed nested tensor / non-nested tensor inputs. "
            "Please file an issue requesting this if it is important to you."
        )

    if (
        (query.is_nested and query._lengths is not None)  # type: ignore[attr-defined]
        or (key.is_nested and key._lengths is not None)  # type: ignore[attr-defined]
        or (value.is_nested and value._lengths is not None)  # type: ignore[attr-defined]
    ):
        raise ValueError(
            "FlexAttention does not support nested tensors that are non-contiguous with holes. "
            "Please file an issue requesting this if it is important to you."
        )

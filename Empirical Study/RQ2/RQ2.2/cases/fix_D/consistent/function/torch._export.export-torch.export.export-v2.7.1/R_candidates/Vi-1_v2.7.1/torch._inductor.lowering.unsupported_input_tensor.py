def unsupported_input_tensor(t: torch.Tensor, parent=None, node=None):
    "Do not support reading or writing to this tensor"
    if t.is_complex():
        # Complex views are supported with IR ComplexView
        if parent and parent.target in (
            torch.ops.aten.view.dtype,
            torch.ops.prims.convert_element_type.default,
        ):
            return False
        _warn_complex_not_supported()
        return True

    if t.dtype == torch.float8_e8m0fnu:
        if not node:
            return True

        # allow bitcast, views, memory movement, but not arithmetic
        # TODO: delete once triton adds native support
        return not (
            node.target
            in (
                aten.view.dtype,
                aten.cat.default,
            )
            or is_view(node.target)
        )

    return False

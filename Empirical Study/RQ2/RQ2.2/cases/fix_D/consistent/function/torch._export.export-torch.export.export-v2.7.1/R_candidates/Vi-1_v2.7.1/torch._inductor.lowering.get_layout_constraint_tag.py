def get_layout_constraint_tag(fn):
    tags_by_priority = [
        torch._C.Tag.needs_fixed_stride_order,
        torch._C.Tag.flexible_layout,
    ]
    for tag in tags_by_priority:
        if tag in fn.tags:
            return tag
    if torch._library.utils.is_builtin(fn):
        return torch._C.Tag.flexible_layout
    return getattr(torch._C.Tag, config.custom_op_default_layout_constraint)

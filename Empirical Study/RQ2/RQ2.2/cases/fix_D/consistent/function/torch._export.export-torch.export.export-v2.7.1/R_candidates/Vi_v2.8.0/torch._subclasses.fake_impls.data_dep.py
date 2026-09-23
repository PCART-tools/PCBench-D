@register_op_impl(lambda func: torch.Tag.data_dependent_output in func.tags)
def data_dep(fake_mode, func, *args, **kwargs):
    raise DataDependentOutputException(func)

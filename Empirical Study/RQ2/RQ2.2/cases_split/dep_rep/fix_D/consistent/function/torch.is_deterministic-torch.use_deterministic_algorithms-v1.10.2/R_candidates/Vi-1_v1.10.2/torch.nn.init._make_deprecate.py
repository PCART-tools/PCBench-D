def _make_deprecate(meth):
    new_name = meth.__name__
    old_name = new_name[:-1]

    def deprecated_init(*args, **kwargs):
        warnings.warn("nn.init.{} is now deprecated in favor of nn.init.{}."
                      .format(old_name, new_name), stacklevel=2)
        return meth(*args, **kwargs)

    deprecated_init.__doc__ = r"""
    {old_name}(...)

    .. warning::
        This method is now deprecated in favor of :func:`torch.nn.init.{new_name}`.

    See :func:`~torch.nn.init.{new_name}` for details.""".format(
        old_name=old_name, new_name=new_name)
    deprecated_init.__name__ = old_name
    return deprecated_init

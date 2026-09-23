@init_once_fakemode
def lazy_init():
    from . import efficient_conv_bn_eval, split_cat  # noqa: F401

    if config.is_fbcode():
        from . import fb  # type: ignore[attr-defined]  # noqa: F401

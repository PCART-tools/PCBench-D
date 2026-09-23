def __getattr__(name):
    return _sub_module_deprecation(sub_package="integrate", module="dop",
                                   private_modules=["_dop"], all=__all__,
                                   attribute=name)

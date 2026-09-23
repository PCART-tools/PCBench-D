def __getattr__(name):
    return _sub_module_deprecation(sub_package="integrate", module="vode",
                                   private_modules=["_vode"], all=__all__,
                                   attribute=name)

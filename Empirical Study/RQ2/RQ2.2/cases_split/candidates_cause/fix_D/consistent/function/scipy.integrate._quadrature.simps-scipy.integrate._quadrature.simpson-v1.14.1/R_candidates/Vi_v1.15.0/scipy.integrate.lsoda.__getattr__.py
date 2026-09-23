def __getattr__(name):
    return _sub_module_deprecation(sub_package="integrate", module="lsoda",
                                   private_modules=["_lsoda"], all=__all__,
                                   attribute=name)

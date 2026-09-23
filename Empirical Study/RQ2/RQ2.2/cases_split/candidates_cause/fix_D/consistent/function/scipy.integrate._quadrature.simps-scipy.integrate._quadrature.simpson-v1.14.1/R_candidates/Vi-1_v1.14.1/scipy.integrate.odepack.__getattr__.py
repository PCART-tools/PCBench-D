def __getattr__(name):
    return _sub_module_deprecation(sub_package="integrate", module="odepack",
                                   private_modules=["_odepack_py"], all=__all__,
                                   attribute=name)

def __getattr__(name):
    return _sub_module_deprecation(sub_package="integrate", module="quadpack",
                                   private_modules=["_quadpack_py"], all=__all__,
                                   attribute=name)

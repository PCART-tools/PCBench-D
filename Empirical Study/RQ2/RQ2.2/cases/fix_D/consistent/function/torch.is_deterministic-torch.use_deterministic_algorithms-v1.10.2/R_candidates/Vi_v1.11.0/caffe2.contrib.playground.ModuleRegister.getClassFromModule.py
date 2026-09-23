def getClassFromModule(moduleName, className):
    myClass = None
    for ModuleMap in MODULE_MAPS:
        for name, obj in inspect.getmembers(ModuleMap):
            if name == moduleName:
                log.info("ModuleRegistry from module {} get class {} of source:{}".
                         format(moduleName, className, inspect.getsource(obj)))
                myClass = getattr(obj, className)
                return myClass
    return None

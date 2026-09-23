def getModule(moduleName):
    log.info("get module {} from MODULE_MAPS content {}".format(moduleName, str(MODULE_MAPS)))
    myModule = None
    for ModuleMap in MODULE_MAPS:
        log.info("iterate through MODULE_MAPS content {}".
                 format(str(ModuleMap)))
        for name, obj in inspect.getmembers(ModuleMap):
            log.info("iterate through MODULE_MAPS a name {}".format(str(name)))
            if name == moduleName:
                log.info("AnyExp get module {} with source:{}".
                         format(moduleName, inspect.getsource(obj)))
                myModule = obj
                return myModule
    return None

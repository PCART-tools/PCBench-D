def registerModuleMap(module_map):
    MODULE_MAPS.append(module_map)
    log.info("ModuleRegister get modules from  ModuleMap content: {}".
             format(inspect.getsource(module_map)))

def overrideAdditionalMethods(myTrainerClass, opts):
    log.info("B4 additional override myTrainerClass source {}".
        format(inspect.getsource(myTrainerClass)))
    # override any additional modules
    myAdditionalOverride = getModule(opts['model']['additional_override_py'])
    if myAdditionalOverride is not None:
        for funcName, funcValue in inspect.getmembers(myAdditionalOverride,
                                                      inspect.isfunction):
            setattr(myTrainerClass, funcName, funcValue)
    log.info("Aft additional override myTrainerClass's source {}".
        format(inspect.getsource(myTrainerClass)))
    return myTrainerClass

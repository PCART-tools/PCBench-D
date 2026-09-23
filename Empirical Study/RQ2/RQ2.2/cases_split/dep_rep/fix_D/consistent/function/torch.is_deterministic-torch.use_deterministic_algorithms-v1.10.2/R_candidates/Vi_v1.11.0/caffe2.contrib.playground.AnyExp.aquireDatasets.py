def aquireDatasets(opts):
    myAquireDataModule = ModuleRegister.getModule(opts['input']['input_name_py'])
    return myAquireDataModule.get_input_dataset(opts)

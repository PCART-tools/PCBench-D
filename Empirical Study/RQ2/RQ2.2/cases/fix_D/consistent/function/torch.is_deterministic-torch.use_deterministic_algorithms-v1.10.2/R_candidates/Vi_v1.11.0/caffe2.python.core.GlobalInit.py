def GlobalInit(args):
    TriggerLazyImport()
    _GLOBAL_INIT_ARGS.extend(args[1:])
    C.global_init(args)

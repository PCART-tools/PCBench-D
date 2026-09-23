def repro_get_args(options, exported_program, config_patches):
    mod, args, kwargs = repro_common(options, exported_program)
    return mod, args, kwargs

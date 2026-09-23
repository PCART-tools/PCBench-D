def repro_common(options, exported_program):
    torch._inductor.config.generate_intermediate_hooks = True
    mod = exported_program.module()
    args, kwargs = exported_program.example_inputs
    return mod, args, kwargs

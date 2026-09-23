def generate_code(ninja_global: Optional[str] = None,
                  nn_path: Optional[str] = None,
                  native_functions_path: Optional[str] = None,
                  install_dir: Optional[str] = None,
                  subset: Optional[str] = None,
                  disable_autograd: bool = False,
                  force_schema_registration: bool = False,
                  operator_selector: Any = None) -> None:
    from tools.autograd.gen_autograd import gen_autograd, gen_autograd_python
    from tools.autograd.gen_annotated_fn_args import gen_annotated
    from tools.codegen.selective_build.selector import SelectiveBuilder


    # Build ATen based Variable classes
    if install_dir is None:
        install_dir = 'torch/csrc'
        python_install_dir = 'torch/testing/_internal/generated'
    else:
        python_install_dir = install_dir
    autograd_gen_dir = os.path.join(install_dir, 'autograd', 'generated')
    jit_gen_dir = os.path.join(install_dir, 'jit', 'generated')
    for d in (autograd_gen_dir, jit_gen_dir, python_install_dir):
        if not os.path.exists(d):
            os.makedirs(d)
    runfiles_dir = os.environ.get("RUNFILES_DIR", None)
    data_dir = os.path.join(runfiles_dir, 'pytorch') if runfiles_dir else ''
    autograd_dir = os.path.join(data_dir, 'tools', 'autograd')
    tools_jit_templates = os.path.join(data_dir, 'tools', 'jit', 'templates')

    if subset == "pybindings" or not subset:
        gen_autograd_python(
            native_functions_path or NATIVE_FUNCTIONS_PATH,
            autograd_gen_dir,
            autograd_dir)

    if operator_selector is None:
        operator_selector = SelectiveBuilder.get_nop_selector()

    if subset == "libtorch" or not subset:

        gen_autograd(
            native_functions_path or NATIVE_FUNCTIONS_PATH,
            autograd_gen_dir,
            autograd_dir,
            disable_autograd=disable_autograd,
            operator_selector=operator_selector,
        )

    if subset == "python" or not subset:
        gen_annotated(
            native_functions_path or NATIVE_FUNCTIONS_PATH,
            python_install_dir,
            autograd_dir)

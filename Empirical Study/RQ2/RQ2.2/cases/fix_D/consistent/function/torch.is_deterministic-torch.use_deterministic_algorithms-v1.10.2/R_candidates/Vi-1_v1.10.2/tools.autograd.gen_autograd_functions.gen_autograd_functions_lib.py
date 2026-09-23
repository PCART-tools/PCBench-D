def gen_autograd_functions_lib(
    out: str,
    differentiability_infos: Sequence[DifferentiabilityInfo],
    template_path: str,
) -> None:
    """Functions.h and Functions.cpp body

    These contain the auto-generated subclasses of torch::autograd::Node
    for each every differentiable torch function.
    """

    # only create an autograd function if we are actually going to calculate a derivative
    infos = list(filter(lambda info: info.args_with_derivatives, differentiability_infos))
    declarations = list(map(lambda f: process_function(f, FUNCTION_DECLARATION), infos))
    definitions = list(map(lambda f: process_function(f, FUNCTION_DEFINITION), infos))

    file_basename = 'Functions'
    fm = FileManager(install_dir=out, template_dir=template_path, dry_run=False)
    for suffix in ['.h', '.cpp']:
        fname = file_basename + suffix
        fm.write_with_template(fname, fname, lambda: {
            'generated_comment': '@' + f'generated from {fm.template_dir}/' + fname,
            'autograd_function_declarations': declarations,
            'autograd_function_definitions': definitions,
        })

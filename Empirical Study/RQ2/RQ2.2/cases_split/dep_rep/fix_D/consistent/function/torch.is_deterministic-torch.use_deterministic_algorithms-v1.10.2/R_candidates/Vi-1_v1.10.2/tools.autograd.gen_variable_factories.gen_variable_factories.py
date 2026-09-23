def gen_variable_factories(out: str, native_yaml_path: str, template_path: str) -> None:
    native_functions = parse_native_yaml(native_yaml_path).native_functions
    fm = FileManager(install_dir=out, template_dir=template_path, dry_run=False)
    fm.write_with_template('variable_factories.h', 'variable_factories.h', lambda: {
        'generated_comment': '@' + f'generated from {fm.template_dir}/variable_factories.h',
        'function_definitions': list(mapMaybe(process_function, native_functions)),
    })

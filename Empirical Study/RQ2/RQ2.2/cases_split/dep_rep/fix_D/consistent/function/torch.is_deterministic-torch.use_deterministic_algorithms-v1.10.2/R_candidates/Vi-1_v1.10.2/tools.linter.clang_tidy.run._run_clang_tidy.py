async def _run_clang_tidy(
    options: Any, line_filters: List[Dict[str, Any]], files: Iterable[str]
) -> CommandResult:
    """Executes the actual clang-tidy command in the shell."""

    base = [options.clang_tidy_exe]

    # Apply common options
    base += ["-p", options.compile_commands_dir]
    if not options.config_file and os.path.exists(".clang-tidy"):
        options.config_file = ".clang-tidy"
    if options.config_file:
        import yaml

        with open(options.config_file) as config:
            # Here we convert the YAML config file to a JSON blob.
            base += [
                "-config",
                json.dumps(yaml.load(config, Loader=yaml.SafeLoader)),
            ]
    if options.print_include_paths:
        base += ["--extra-arg", "-v"]
    if options.include_dir:
        for dir in options.include_dir:
            base += ["--extra-arg", f"-I{dir}"]
    base += options.extra_args
    if line_filters:
        base += ["-line-filter", json.dumps(line_filters)]

    # Apply per-file options
    commands = []
    for f in files:
        command = list(base) + [map_filename(options.compile_commands_dir, f)]
        commands.append((command, f))

    if options.dry_run:
        return CommandResult(0, str([c for c, _ in commands]), "")

    return await _run_clang_tidy_in_parallel(commands, options.disable_progress_bar)

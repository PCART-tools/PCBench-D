async def _run(options: Any) -> Tuple[CommandResult, List[ClangTidyWarning]]:
    # These flags are pervasive enough to set it globally. It makes the code
    # cleaner compared to threading it through every single function.
    global VERBOSE
    global QUIET
    VERBOSE = options.verbose
    QUIET = options.quiet

    # Normalize the paths first
    paths = [path.rstrip("/") for path in options.paths]

    # Filter files
    if options.diff_file:
        files, line_filters = filter_from_diff_file(options.paths, options.diff_file)
    else:
        files, line_filters = await filter_default(options.paths)

    file_patterns = get_file_patterns(options.glob, options.regex)
    files = list(filter_files(files, file_patterns))

    # clang-tidy errors when it does not get input files.
    if not files:
        log("No files detected")
        return CommandResult(0, "", ""), []

    result = await _run_clang_tidy(options, line_filters, files)
    fixes, warnings = extract_warnings(
        result.stdout, base_dir=options.compile_commands_dir
    )

    if options.suppress_diagnostics:
        for fname in fixes.keys():
            mapped_fname = map_filename(options.compile_commands_dir, fname)
            log(f"Applying fixes to {mapped_fname}")
            apply_nolint(fname, fixes[fname])
            if os.path.relpath(fname) != mapped_fname:
                shutil.copyfile(fname, mapped_fname)

    if options.dry_run:
        log(result)
    elif result.failed():
        # If you change this message, update the error checking logic in
        # .github/workflows/lint.yml
        msg = "Warnings detected!"
        log(msg)
        log("Summary:")
        for w in warnings:
            log(str(w))

    return result, warnings

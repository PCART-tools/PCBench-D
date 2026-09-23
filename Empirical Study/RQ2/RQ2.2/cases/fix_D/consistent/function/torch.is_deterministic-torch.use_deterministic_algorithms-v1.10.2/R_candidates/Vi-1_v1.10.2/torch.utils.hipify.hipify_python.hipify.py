def hipify(
    project_directory: str,
    show_detailed: bool = False,
    extensions: Iterable = (".cu", ".cuh", ".c", ".cc", ".cpp", ".h", ".in", ".hpp"),
    output_directory: str = "",
    includes: Iterable = (),
    extra_files: Iterable = (),
    out_of_place_only: bool = False,
    ignores: Iterable = (),
    show_progress: bool = True,
    hip_clang_launch: bool = False,
    is_pytorch_extension: bool = False,
    clean_ctx: GeneratedFileCleaner = None
) -> HipifyFinalResult:
    if project_directory == "":
        project_directory = os.getcwd()

    # Verify the project directory exists.
    if not os.path.exists(project_directory):
        print("The project folder specified does not exist.")
        sys.exit(1)

    # If no output directory, provide a default one.
    if not output_directory:
        project_directory.rstrip("/")
        output_directory = project_directory + "_amd"

    # Copy from project directory to output directory if not done already.
    if not os.path.exists(output_directory):
        shutil.copytree(project_directory, output_directory)

    all_files = list(matched_files_iter(output_directory, includes=includes,
                                        ignores=ignores, extensions=extensions,
                                        out_of_place_only=out_of_place_only,
                                        is_pytorch_extension=is_pytorch_extension))
    all_files_set = set(all_files)
    # Convert extra_files to relative paths since all_files has all relative paths
    for f in extra_files:
        f_rel = os.path.relpath(f, output_directory)
        if f_rel not in all_files_set:
            all_files.append(f_rel)

    # Start Preprocessor
    return preprocess(
        output_directory,
        all_files,
        includes,
        show_detailed=show_detailed,
        show_progress=show_progress,
        hip_clang_launch=hip_clang_launch,
        is_pytorch_extension=is_pytorch_extension,
        clean_ctx=clean_ctx)

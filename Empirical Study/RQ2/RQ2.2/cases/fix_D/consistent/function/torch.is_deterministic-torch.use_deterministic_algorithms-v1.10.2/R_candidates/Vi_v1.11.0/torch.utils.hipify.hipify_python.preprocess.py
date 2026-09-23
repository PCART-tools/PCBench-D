def preprocess(
        output_directory: str,
        all_files: Iterable,
        includes: Iterable,
        show_detailed: bool = False,
        show_progress: bool = True,
        hip_clang_launch: bool = False,
        is_pytorch_extension: bool = False,
        clean_ctx: Optional[GeneratedFileCleaner] = None) -> HipifyFinalResult:
    """
    Call preprocessor on selected files.

    Arguments)
        show_detailed - Show a detailed summary of the transpilation process.
    """

    if clean_ctx is None:
        clean_ctx = GeneratedFileCleaner(keep_intermediates=True)

    # Preprocessing statistics.
    stats: Dict[str, List] = {"unsupported_calls": [], "kernel_launches": []}

    for filepath in all_files:
        preprocess_file_and_save_result(output_directory, filepath, all_files, includes, stats,
                                        hip_clang_launch, is_pytorch_extension, clean_ctx, show_progress)

    print(bcolors.OKGREEN + "Successfully preprocessed all matching files." + bcolors.ENDC, file=sys.stderr)

    # Show detailed summary
    if show_detailed:
        compute_stats(stats)

    return HIPIFY_FINAL_RESULT

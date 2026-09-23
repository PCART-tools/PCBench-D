def preprocess_file_and_save_result(
        output_directory: str,
        filepath: str,
        all_files: Iterable,
        includes: Iterable,
        stats: Dict[str, List],
        hip_clang_launch: bool,
        is_pytorch_extension: bool,
        clean_ctx: GeneratedFileCleaner,
        show_progress: bool) -> None:
    result = preprocessor(output_directory, filepath, all_files, includes, stats,
                          hip_clang_launch, is_pytorch_extension, clean_ctx, show_progress)

    fin_path = os.path.abspath(os.path.join(output_directory, filepath))
    # Show what happened
    if show_progress:
        print(
            fin_path, "->",
            result["hipified_path"], result["status"])

    if result["hipified_path"] is not None:
        HIPIFY_FINAL_RESULT[fin_path] = result

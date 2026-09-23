def preprocessor(
        output_directory: str,
        filepath: str,
        all_files: Iterable,
        includes: Iterable,
        stats: Dict[str, List],
        hip_clang_launch: bool,
        is_pytorch_extension: bool,
        clean_ctx: GeneratedFileCleaner,
        show_progress: bool) -> HipifyResult:
    """ Executes the CUDA -> HIP conversion on the specified file. """
    fin_path = os.path.abspath(os.path.join(output_directory, filepath))

    with open(fin_path, 'r', encoding='utf-8') as fin:
        if fin.readline() == HIPIFY_C_BREADCRUMB:
            return {"hipified_path": None, "status": "ignored"}
        fin.seek(0)
        output_source = fin.read()

    orig_output_source = output_source

    fout_path = os.path.abspath(os.path.join(output_directory, get_hip_file_path(filepath, is_pytorch_extension)))
    if not os.path.exists(os.path.dirname(fout_path)):
        clean_ctx.makedirs(os.path.dirname(fout_path))

    # unsupported_calls statistics reporting is broken atm
    def pt_repl(m):
        return PYTORCH_MAP[m.group(0)]

    if is_pytorch_extension:
        output_source = RE_PYTORCH_PREPROCESSOR.sub(pt_repl, output_source)
    else:
        if is_pytorch_file(filepath):
            output_source = RE_PYTORCH_PREPROCESSOR.sub(pt_repl, output_source)
        else:
            def c2_repl(m):
                return CAFFE2_MAP[m.group(0)]
            output_source = RE_CAFFE2_PREPROCESSOR.sub(c2_repl, output_source)

    # Header rewrites
    def mk_repl(templ, include_current_dir=True):
        def repl(m):
            f = m.group(1)
            dirpath, filename = os.path.split(f)
            if (
                f.startswith("ATen/cuda")
                or f.startswith("ATen/native/cuda")
                or f.startswith("ATen/native/quantized/cuda")
                or f.startswith("ATen/native/sparse/cuda")
                or f.startswith("THC/")
                or (f.startswith("THC") and not f.startswith("THCP"))
            ):
                return templ.format(get_hip_file_path(m.group(1), is_pytorch_extension))
            # if filename is one of the files being hipified for this extension
            if (is_pytorch_extension and any(s.endswith(filename) for s in all_files)):
                header_dir = None
                header_filepath = None
                # If include_current_dir True, look first in same dir as the including source file
                if include_current_dir:
                    header_dir_to_check = os.path.dirname(fin_path)
                    header_path_to_check = os.path.abspath(os.path.join(header_dir_to_check, f))
                    if os.path.exists(header_path_to_check):
                        header_dir = header_dir_to_check
                        header_filepath = header_path_to_check
                # If not found, look in include dirs one by one and first match wins
                if header_filepath is None:
                    for include in includes:
                        header_dir_to_check = os.path.join(output_directory, os.path.dirname(include))
                        header_path_to_check = os.path.abspath(os.path.join(header_dir_to_check, f))
                        if os.path.exists(header_path_to_check):
                            header_dir = header_dir_to_check
                            header_filepath = header_path_to_check
                # If header file not found, keep as is
                if header_filepath is None:
                    return m.group(0)
                # Hipify header file first if needed
                if header_filepath not in HIPIFY_FINAL_RESULT:
                    preprocess_file_and_save_result(output_directory,
                                                    os.path.relpath(header_filepath, output_directory),
                                                    all_files, includes, stats, hip_clang_launch, is_pytorch_extension,
                                                    clean_ctx, show_progress)
                value = HIPIFY_FINAL_RESULT[header_filepath]["hipified_path"]
                assert value is not None
                return templ.format(os.path.relpath(value, header_dir))

            return m.group(0)
        return repl
    output_source = RE_QUOTE_HEADER.sub(mk_repl('#include "{0}"', True), output_source)
    output_source = RE_ANGLE_HEADER.sub(mk_repl('#include <{0}>', False), output_source)
    output_source = RE_THC_GENERIC_FILE.sub(mk_repl('#define THC_GENERIC_FILE "{0}"'), output_source)

    # CMakeLists.txt rewrites
    if filepath.endswith('CMakeLists.txt'):
        output_source = output_source.replace('CUDA', 'HIP')
        output_source = output_source.replace('THC', 'THH')
        output_source = RE_CU_SUFFIX.sub('.hip', output_source)

    # Perform Kernel Launch Replacements
    if not hip_clang_launch:
        output_source = processKernelLaunches(output_source, stats)

    # Replace std:: with non-std:: versions
    if (filepath.endswith(".cu") or filepath.endswith(".cuh")) and "PowKernel" not in filepath:
        output_source = replace_math_functions(output_source)

    # Include header if device code is contained.
    output_source = hip_header_magic(output_source)

    # Replace the extern __shared__
    output_source = replace_extern_shared(output_source)

    # Don't write out identical hipified files for extensions if dirpath has not changed
    if (
        is_pytorch_extension
        and orig_output_source == output_source
        and os.path.dirname(fin_path) == os.path.dirname(fout_path)
    ):
        return {"hipified_path": fin_path, "status": "ok"}

    # Add hipify breadcrumb for C-style files to avoid re-hipification
    if fin_path != fout_path and match_extensions(fin_path, (".cu", ".cuh", ".c", ".cc", ".cpp", ".h", ".hpp")):
        output_source = HIPIFY_C_BREADCRUMB + output_source

    do_write = True
    if os.path.exists(fout_path):
        with open(fout_path, 'r', encoding='utf-8') as fout_old:
            do_write = fout_old.read() != output_source
    if do_write:
        try:
            with clean_ctx.open(fout_path, 'w', encoding='utf-8') as fout:
                fout.write(output_source)
            return {"hipified_path": fout_path, "status": "ok"}
        except PermissionError as e:
            print(f"{bcolors.WARNING}Failed to save {fout_path} with \"{e.strerror}\", leaving {fin_path} unchanged.{bcolors.ENDC}",
                  file=sys.stderr)
            return {"hipified_path": fin_path, "status": "skipped"}
    else:
        return {"hipified_path": fout_path, "status": "skipped"}

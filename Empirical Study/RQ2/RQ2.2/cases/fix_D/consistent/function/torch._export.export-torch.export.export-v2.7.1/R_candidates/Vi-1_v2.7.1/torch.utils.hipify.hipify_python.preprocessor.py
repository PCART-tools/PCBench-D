def preprocessor(
        output_directory: str,
        filepath: str,
        all_files: Iterable,
        header_include_dirs: Iterable,
        stats: dict[str, list],
        hip_clang_launch: bool,
        is_pytorch_extension: bool,
        clean_ctx: GeneratedFileCleaner,
        show_progress: bool) -> HipifyResult:
    """ Executes the CUDA -> HIP conversion on the specified file. """
    fin_path = os.path.abspath(os.path.join(output_directory, filepath))
    hipify_result = HIPIFY_FINAL_RESULT[fin_path]
    if filepath not in all_files:
        hipify_result.hipified_path = None
        hipify_result.status = "[ignored, not to be hipified]"
        hipify_result.current_state = CurrentState.DONE
        return hipify_result

    rel_filepath = _to_unix_path(os.path.relpath(filepath, output_directory))

    with open(fin_path, encoding='utf-8') as fin:
        if fin.readline() == HIPIFY_C_BREADCRUMB:
            hipify_result.hipified_path = None
            hipify_result.status = "[ignored, input is hipified output]"
            hipify_result.current_state = CurrentState.DONE
            return hipify_result
        fin.seek(0)
        output_source = fin.read()

    orig_output_source = output_source

    # get_hip_file_path needs a relative path to work correctly
    fout_path = os.path.abspath(os.path.join(output_directory, get_hip_file_path(rel_filepath, is_pytorch_extension)))
    if not os.path.exists(os.path.dirname(fout_path)):
        clean_ctx.makedirs(os.path.dirname(fout_path))

    # unsupported_calls statistics reporting is broken atm
    def pt_repl(m):
        return PYTORCH_MAP[m.group(0)]

    def pt_special_repl(m):
        # checks SPECIAL map first, and if a miss occurs, falls back to pytorch mappings
        return PYTORCH_SPECIAL_MAP.get(m.group(0), pt_repl(m))


    if is_pytorch_extension:
        output_source = RE_PYTORCH_PREPROCESSOR.sub(pt_repl, output_source)
    else:
        if is_special_file(rel_filepath):
            output_source = RE_PYTORCH_PREPROCESSOR.sub(pt_special_repl, output_source)
        elif is_pytorch_file(rel_filepath):
            output_source = RE_PYTORCH_PREPROCESSOR.sub(pt_repl, output_source)
        else:
            def c2_repl(m):
                return CAFFE2_MAP[m.group(0)]
            output_source = RE_CAFFE2_PREPROCESSOR.sub(c2_repl, output_source)

    # Header rewrites
    def mk_repl(templ, include_current_dir=True):
        def repl(m):
            f = m.group(1)
            filename = os.path.basename(f)
            if (
                f.startswith(("ATen/cuda",
                              "ATen/native/cuda",
                              "ATen/native/nested/cuda",
                              "ATen/native/quantized/cuda",
                              "ATen/native/sparse/cuda",
                              "ATen/native/transformers/cuda",
                              "THC/")) or
                (f.startswith("THC") and not f.startswith("THCP"))
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
                    for header_include_dir in header_include_dirs:
                        header_dir_to_check = os.path.join(output_directory, header_include_dir)
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
                                                    header_filepath,
                                                    all_files, header_include_dirs, stats, hip_clang_launch,
                                                    is_pytorch_extension, clean_ctx, show_progress)
                elif header_filepath in HIPIFY_FINAL_RESULT:
                    header_result = HIPIFY_FINAL_RESULT[header_filepath]
                    if header_result.current_state == CurrentState.INITIALIZED:
                        # get_hip_file_path needs a relative path to work correctly
                        header_rel_path = os.path.relpath(header_filepath, output_directory)
                        header_fout_path = os.path.abspath(os.path.join(output_directory,
                                                                        get_hip_file_path(header_rel_path, is_pytorch_extension)))
                        header_result.hipified_path = header_fout_path
                        HIPIFY_FINAL_RESULT[header_filepath] = header_result
                        return templ.format(os.path.relpath(header_fout_path if header_fout_path is not None
                                                            else header_filepath, header_dir))
                hipified_header_filepath = HIPIFY_FINAL_RESULT[header_filepath].hipified_path
                return templ.format(os.path.relpath(hipified_header_filepath if hipified_header_filepath is not None
                                                    else header_filepath, header_dir))

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
    if (filepath.endswith((".cu", ".cuh"))) and "PowKernel" not in filepath:
        output_source = replace_math_functions(output_source)

    # Include header if device code is contained.
    output_source = hip_header_magic(output_source)

    # Replace the extern __shared__
    # NOTE: No longer needed after transition from hcc to hipclang.
    # output_source = replace_extern_shared(output_source)

    # Don't write out identical hipified files for extensions if dirpath has not changed
    if (
        is_pytorch_extension
        and orig_output_source == output_source
        and os.path.dirname(fin_path) == os.path.dirname(fout_path)
    ):
        hipify_result.hipified_path = fin_path
        hipify_result.status = "[skipped, no changes]"
        hipify_result.current_state = CurrentState.DONE
        return hipify_result

    # Add hipify breadcrumb for C-style files to avoid re-hipification
    if fin_path != fout_path and match_extensions(fin_path, (".cu", ".cuh", ".c", ".cc", ".cpp", ".h", ".hpp")):
        output_source = HIPIFY_C_BREADCRUMB + output_source

    do_write = True
    if os.path.exists(fout_path):
        with open(fout_path, encoding='utf-8') as fout_old:
            do_write = fout_old.read() != output_source
    if do_write:
        try:
            with clean_ctx.open(fout_path, 'w', encoding='utf-8') as fout:
                fout.write(output_source)
            hipify_result.hipified_path = fout_path
            hipify_result.status = "[ok]"
            hipify_result.current_state = CurrentState.DONE
            return hipify_result
        except PermissionError as e:
            print(f'{bcolors.WARNING}Failed to save {fout_path} with "{e.strerror}", leaving {fin_path} unchanged.{bcolors.ENDC}',
                  file=sys.stderr)
            hipify_result.hipified_path = fin_path
            hipify_result.status = "[skipped, no permissions]"
            hipify_result.current_state = CurrentState.DONE
            return hipify_result
    else:
        hipify_result.hipified_path = fout_path
        hipify_result.status = "[skipped, already hipified]"
        hipify_result.current_state = CurrentState.DONE
        return hipify_result

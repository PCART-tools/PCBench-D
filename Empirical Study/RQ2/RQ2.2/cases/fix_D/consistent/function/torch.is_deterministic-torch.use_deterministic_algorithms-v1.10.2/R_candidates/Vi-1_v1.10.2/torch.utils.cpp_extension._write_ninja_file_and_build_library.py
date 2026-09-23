def _write_ninja_file_and_build_library(
        name,
        sources: List[str],
        extra_cflags,
        extra_cuda_cflags,
        extra_ldflags,
        extra_include_paths,
        build_directory: str,
        verbose: bool,
        with_cuda: Optional[bool],
        is_standalone: bool = False) -> None:
    verify_ninja_availability()
    if IS_WINDOWS:
        compiler = os.environ.get('CXX', 'cl')
    else:
        compiler = os.environ.get('CXX', 'c++')
    check_compiler_abi_compatibility(compiler)
    if with_cuda is None:
        with_cuda = any(map(_is_cuda_file, sources))
    extra_ldflags = _prepare_ldflags(
        extra_ldflags or [],
        with_cuda,
        verbose,
        is_standalone)
    build_file_path = os.path.join(build_directory, 'build.ninja')
    if verbose:
        print(f'Emitting ninja build file {build_file_path}...')
    # NOTE: Emitting a new ninja build file does not cause re-compilation if
    # the sources did not change, so it's ok to re-emit (and it's fast).
    _write_ninja_file_to_build_library(
        path=build_file_path,
        name=name,
        sources=sources,
        extra_cflags=extra_cflags or [],
        extra_cuda_cflags=extra_cuda_cflags or [],
        extra_ldflags=extra_ldflags or [],
        extra_include_paths=extra_include_paths or [],
        with_cuda=with_cuda,
        is_standalone=is_standalone)

    if verbose:
        print(f'Building extension module {name}...')
    _run_ninja_build(
        build_directory,
        verbose,
        error_prefix=f"Error building extension '{name}'")

def get_cpp_options(
    cpp_compiler: str,
    do_link: bool,
    warning_all: bool = True,
    extra_flags: Sequence[str] = (),
    min_optimize: bool = False,
) -> tuple[list[str], list[str], list[str], list[str], list[str], list[str], list[str]]:
    definitions: list[str] = []
    include_dirs: list[str] = []
    cflags: list[str] = []
    ldflags: list[str] = []
    libraries_dirs: list[str] = []
    libraries: list[str] = []
    passthrough_args: list[str] = []

    cflags = (
        _get_shared_cflag(do_link)
        + _get_optimization_cflags(cpp_compiler, min_optimize)
        + _get_warning_all_cflag(warning_all)
        + _get_cpp_std_cflag()
        + _get_os_related_cpp_cflags(cpp_compiler)
    )

    passthrough_args.append(" ".join(extra_flags))

    return (
        definitions,
        include_dirs,
        cflags,
        ldflags,
        libraries_dirs,
        libraries,
        passthrough_args,
    )

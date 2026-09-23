def _get_os_related_cpp_cflags(cpp_compiler: str) -> list[str]:
    if _IS_WINDOWS:
        cflags = [
            "wd4819",
            "wd4251",
            "wd4244",
            "wd4267",
            "wd4275",
            "wd4018",
            "wd4190",
            "wd4624",
            "wd4067",
            "wd4068",
            "EHsc",
        ]
    else:
        cflags = ["Wno-unused-variable", "Wno-unknown-pragmas"]
        if _is_clang(cpp_compiler):
            ignored_optimization_argument = (
                "Werror=ignored-optimization-argument"
                if config.aot_inductor.raise_error_on_ignored_optimization
                else "Wno-ignored-optimization-argument"
            )
            cflags.append(ignored_optimization_argument)
    return cflags

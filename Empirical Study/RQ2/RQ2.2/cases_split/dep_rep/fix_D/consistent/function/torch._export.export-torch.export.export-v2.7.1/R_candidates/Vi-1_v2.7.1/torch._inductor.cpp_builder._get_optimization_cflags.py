def _get_optimization_cflags(
    cpp_compiler: str, min_optimize: bool = False
) -> list[str]:
    if _IS_WINDOWS:
        return ["O1" if min_optimize else "O2"]
    else:
        cflags = (
            ["O0", "g"]
            if config.aot_inductor.debug_compile
            else ["O1" if min_optimize else "O3", "DNDEBUG"]
        )
        cflags += _get_ffast_math_flags()
        cflags.append("fno-finite-math-only")
        if not config.cpp.enable_unsafe_math_opt_flag:
            cflags.append("fno-unsafe-math-optimizations")
        cflags.append(f"ffp-contract={config.cpp.enable_floating_point_contract_flag}")

        if sys.platform != "darwin":
            # on macos, unknown argument: '-fno-tree-loop-vectorize'
            if _is_gcc(cpp_compiler):
                cflags.append("fno-tree-loop-vectorize")
            # https://stackoverflow.com/questions/65966969/why-does-march-native-not-work-on-apple-m1
            # `-march=native` is unrecognized option on M1
            if not config.is_fbcode():
                if platform.machine() == "ppc64le":
                    cflags.append("mcpu=native")
                else:
                    cflags.append("march=native")

        return cflags

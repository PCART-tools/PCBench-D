def check_compiler_type(cov_type: Optional[CompilerType]) -> None:
    if cov_type is not None and cov_type in [CompilerType.GCC, CompilerType.CLANG]:
        return
    raise Exception(
        f"Can't parse compiler type: {cov_type}.",
        " Please set environment variable COMPILER_TYPE as CLANG or GCC",
    )

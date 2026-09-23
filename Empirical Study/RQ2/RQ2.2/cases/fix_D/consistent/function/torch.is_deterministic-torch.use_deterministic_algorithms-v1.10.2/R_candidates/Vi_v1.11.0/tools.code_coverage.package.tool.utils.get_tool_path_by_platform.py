def get_tool_path_by_platform(platform: TestPlatform) -> str:
    if platform == TestPlatform.FBCODE:
        from caffe2.fb.code_coverage.tool.package.fbcode.utils import get_llvm_tool_path  # type: ignore[import]

        return get_llvm_tool_path()  # type: ignore[no-any-return]
    else:
        from ..oss.utils import get_llvm_tool_path  # type: ignore[no-redef]

        return get_llvm_tool_path()  # type: ignore[no-any-return]

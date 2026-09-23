def detect_compiler_type(platform: TestPlatform) -> CompilerType:
    if platform == TestPlatform.OSS:
        from package.oss.utils import detect_compiler_type  # type: ignore[misc]

        cov_type = detect_compiler_type()  # type: ignore[call-arg]
    else:
        from caffe2.fb.code_coverage.tool.package.fbcode.utils import (  # type: ignore[import]
            detect_compiler_type,
        )

        cov_type = detect_compiler_type()

    check_compiler_type(cov_type)
    return cov_type

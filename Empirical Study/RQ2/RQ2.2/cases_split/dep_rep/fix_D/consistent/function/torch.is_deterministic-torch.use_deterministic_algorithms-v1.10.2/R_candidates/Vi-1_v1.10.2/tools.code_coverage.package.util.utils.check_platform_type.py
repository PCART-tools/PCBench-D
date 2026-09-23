def check_platform_type(platform_type: TestPlatform) -> None:
    if platform_type in [TestPlatform.OSS, TestPlatform.FBCODE]:
        return
    raise Exception(
        f"Can't parse platform type: {platform_type}.",
        " Please set environment variable COMPILER_TYPE as OSS or FBCODE",
    )

def get_and_check_clang_format(verbose: bool = False) -> bool:
    return bool(download("clang-format", CLANG_FORMAT_DIR, PLATFORM_TO_CF_URL, PLATFORM_TO_HASH))

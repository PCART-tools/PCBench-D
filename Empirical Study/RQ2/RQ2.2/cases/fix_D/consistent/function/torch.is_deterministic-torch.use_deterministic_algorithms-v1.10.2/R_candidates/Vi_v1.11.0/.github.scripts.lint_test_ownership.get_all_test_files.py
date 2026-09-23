def get_all_test_files() -> List[Path]:
    test_files = list(TEST_DIR.glob("**/test_*.py"))
    test_files.extend(list(TEST_DIR.glob("**/*_test.py")))
    return [f for f in test_files if not any([fnmatch.fnmatch(str(f), g) for g in GLOB_EXCEPTIONS])]

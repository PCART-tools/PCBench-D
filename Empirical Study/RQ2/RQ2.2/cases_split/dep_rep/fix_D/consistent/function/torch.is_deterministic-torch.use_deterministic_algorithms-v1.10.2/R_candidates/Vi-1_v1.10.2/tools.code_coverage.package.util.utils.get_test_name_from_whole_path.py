def get_test_name_from_whole_path(path: str) -> str:
    # code_coverage_tool/profile/merged/haha.merged -> haha
    start = path.rfind("/")
    end = path.rfind(".")
    assert start >= 0 and end >= 0
    return path[start + 1 : end]

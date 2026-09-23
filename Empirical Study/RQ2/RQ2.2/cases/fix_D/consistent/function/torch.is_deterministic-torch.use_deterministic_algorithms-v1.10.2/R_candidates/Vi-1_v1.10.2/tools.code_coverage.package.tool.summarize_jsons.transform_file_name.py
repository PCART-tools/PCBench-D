def transform_file_name(
    file_path: str, interested_folders: List[str], platform: TestPlatform
) -> str:
    remove_patterns: Set[str] = {".DEFAULT.cpp", ".AVX.cpp", ".AVX2.cpp"}
    for pattern in remove_patterns:
        file_path = file_path.replace(pattern, "")
    # if user has specifiled interested folder
    if interested_folders:
        for folder in interested_folders:
            if folder in file_path:
                return file_path[file_path.find(folder) :]
    # remove pytorch base folder path
    if platform == TestPlatform.OSS:
        from package.oss.utils import get_pytorch_folder

        pytorch_foler = get_pytorch_folder()
        assert file_path.startswith(pytorch_foler)
        file_path = file_path[len(pytorch_foler) + 1 :]
    return file_path

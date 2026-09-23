def create_corresponding_folder(
    cur_path: str, prefix_cur_path: str, dir_list: List[str], new_base_folder: str
) -> None:
    for dir_name in dir_list:
        relative_path = convert_to_relative_path(
            cur_path, prefix_cur_path
        )  # get folder name like 'aten'
        new_folder_path = os.path.join(new_base_folder, relative_path, dir_name)
        create_folder(new_folder_path)

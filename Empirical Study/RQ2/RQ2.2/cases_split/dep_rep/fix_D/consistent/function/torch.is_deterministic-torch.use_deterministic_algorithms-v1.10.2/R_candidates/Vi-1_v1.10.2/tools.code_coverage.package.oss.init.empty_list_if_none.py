def empty_list_if_none(arg_interested_folder: Optional[List[str]]) -> List[str]:
    if arg_interested_folder is None:
        return []
    # if this argument is specified, just return itself
    return arg_interested_folder

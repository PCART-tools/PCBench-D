def list_without(in_list: List[str], without: List[str]) -> List[str]:
    return [item for item in in_list if item not in without]

def sort_upgrader(upgrader_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    sorted_upgrader_list = sorted(upgrader_list, key=lambda one_upgrader: next(iter(one_upgrader)))
    return sorted_upgrader_list

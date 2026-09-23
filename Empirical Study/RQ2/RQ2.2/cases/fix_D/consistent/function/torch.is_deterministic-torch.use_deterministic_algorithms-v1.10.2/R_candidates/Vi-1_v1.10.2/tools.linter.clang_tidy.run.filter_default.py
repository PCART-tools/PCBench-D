async def filter_default(paths: List[str]) -> Tuple[List[str], List[Dict[Any, Any]]]:
    return await get_all_files(paths), []

def snip_if(is_pr: bool, versions: List[str]) -> List[str]:
    """
    Return the full list of versions, or just the latest if on a PR.
    """
    return [versions[-1]] if is_pr else versions

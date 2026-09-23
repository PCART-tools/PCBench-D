def files_mentioned(command: str) -> List[str]:
    """
    Return fully-qualified names of all tmp files referenced by command.
    """
    return [f'/tmp/{match.group(1)}' for match in re.finditer(re_tmp, command)]

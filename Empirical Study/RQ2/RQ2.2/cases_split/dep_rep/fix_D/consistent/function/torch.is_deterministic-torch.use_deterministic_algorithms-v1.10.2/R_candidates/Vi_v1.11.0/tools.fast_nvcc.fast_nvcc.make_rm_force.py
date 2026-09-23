def make_rm_force(commands: List[str]) -> List[str]:
    """
    Add --force to all rm commands.
    """
    return [f'{c} --force' if c.startswith('rm ') else c for c in commands]

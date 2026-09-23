def print_verbose_output(
    *,
    env: Dict[str, str],
    commands: List[List[str]],
    filename: str,
) -> None:
    """
    Human-readably write nvcc --dryrun data to stderr.
    """
    padding = len(str(len(commands) - 1))
    with open(filename, 'w') as f:
        for name, val in env.items():
            print(f'#{" "*padding}$ {name}={val}', file=f)
        for i, command in enumerate(commands):
            prefix = f'{str(i).rjust(padding)}$ '
            print(f'#{prefix}{command[0]}', file=f)
            for part in command[1:]:
                print(f'#{" "*len(prefix)}{part}', file=f)

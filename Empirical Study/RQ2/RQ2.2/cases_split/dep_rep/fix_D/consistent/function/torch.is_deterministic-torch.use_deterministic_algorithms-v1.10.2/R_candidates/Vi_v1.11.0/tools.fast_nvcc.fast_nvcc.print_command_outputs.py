def print_command_outputs(command_results: List[Result]) -> None:
    """
    Print captured stdout and stderr from commands.
    """
    for result in command_results:
        sys.stdout.write(result.get('stdout', b'').decode('ascii'))
        sys.stderr.write(result.get('stderr', b'').decode('ascii'))

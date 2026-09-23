def nvcc_dryrun_data(binary: str, args: List[str]) -> DryunData:
    """
    Return parsed environment variables and commands from nvcc --dryrun.
    """
    result = subprocess.run(  # type: ignore[call-overload]
        [binary, '--dryrun'] + args,
        capture_output=True,
        encoding='ascii',  # this is just a guess
    )
    print(result.stdout, end='')
    env = {}
    commands = []
    for line in result.stderr.splitlines():
        match = re.match(r'^#\$ (.*)$', line)
        if match:
            stripped, = match.groups()
            mapping = re.match(r'^(\w+)=(.*)$', stripped)
            if mapping:
                name, val = mapping.groups()
                env[name] = val
            else:
                commands.append(stripped)
        else:
            print(line, file=sys.stderr)
    return {'env': env, 'commands': commands, 'exit_code': result.returncode}

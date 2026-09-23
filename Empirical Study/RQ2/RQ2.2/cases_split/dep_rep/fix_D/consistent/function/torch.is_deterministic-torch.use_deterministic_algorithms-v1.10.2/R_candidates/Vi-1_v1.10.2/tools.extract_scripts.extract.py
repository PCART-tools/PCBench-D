def extract(step: Step) -> Optional[Script]:
    run = step.get('run')

    # https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#using-a-specific-shell
    shell = step.get('shell', 'bash')
    extension = {
        'bash': '.sh',
        'pwsh': '.ps1',
        'python': '.py',
        'sh': '.sh',
        'cmd': '.cmd',
        'powershell': '.ps1',
    }.get(shell)

    is_gh_script = step.get('uses', '').startswith('actions/github-script@')
    gh_script = step.get('with', {}).get('script')

    if run is not None and extension is not None:
        script = {
            'bash': f'#!/usr/bin/env bash\nset -eo pipefail\n{run}',
            'sh': f'#!/usr/bin/env sh\nset -e\n{run}',
        }.get(shell, run)
        return {'extension': extension, 'script': script}
    elif is_gh_script and gh_script is not None:
        return {'extension': '.js', 'script': gh_script}
    else:
        return None

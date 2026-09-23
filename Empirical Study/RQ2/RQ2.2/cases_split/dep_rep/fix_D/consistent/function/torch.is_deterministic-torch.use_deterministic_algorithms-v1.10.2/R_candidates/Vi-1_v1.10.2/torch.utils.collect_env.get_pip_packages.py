def get_pip_packages(run_lambda):
    """Returns `pip list` output. Note: will also find conda-installed pytorch
    and numpy packages."""
    # People generally have `pip` as `pip` or `pip3`
    # But here it is incoved as `python -mpip`
    def run_with_pip(pip):
        if get_platform() == 'win32':
            system_root = os.environ.get('SYSTEMROOT', 'C:\\Windows')
            findstr_cmd = os.path.join(system_root, 'System32', 'findstr')
            grep_cmd = r'{} /R "numpy torch mypy"'.format(findstr_cmd)
        else:
            grep_cmd = r'grep "torch\|numpy\|mypy"'
        return run_and_read_all(run_lambda, pip + ' list --format=freeze | ' + grep_cmd)

    pip_version = 'pip3' if sys.version[0] == '3' else 'pip'
    out = run_with_pip(sys.executable + ' -mpip')

    return pip_version, out

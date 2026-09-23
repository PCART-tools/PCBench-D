def get_conda_packages(run_lambda):
    if get_platform() == 'win32':
        system_root = os.environ.get('SYSTEMROOT', 'C:\\Windows')
        findstr_cmd = os.path.join(system_root, 'System32', 'findstr')
        grep_cmd = r'{} /R "torch numpy cudatoolkit soumith mkl magma mypy"'.format(findstr_cmd)
    else:
        grep_cmd = r'grep "torch\|numpy\|cudatoolkit\|soumith\|mkl\|magma\|mypy"'
    conda = os.environ.get('CONDA_EXE', 'conda')
    out = run_and_read_all(run_lambda, conda + ' list | ' + grep_cmd)
    if out is None:
        return out
    # Comment starting at beginning of line
    comment_regex = re.compile(r'^#.*\n')
    return re.sub(comment_regex, '', out)

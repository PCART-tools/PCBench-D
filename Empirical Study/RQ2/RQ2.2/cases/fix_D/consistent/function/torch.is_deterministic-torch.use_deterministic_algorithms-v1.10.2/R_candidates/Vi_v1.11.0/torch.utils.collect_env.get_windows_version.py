def get_windows_version(run_lambda):
    system_root = os.environ.get('SYSTEMROOT', 'C:\\Windows')
    wmic_cmd = os.path.join(system_root, 'System32', 'Wbem', 'wmic')
    findstr_cmd = os.path.join(system_root, 'System32', 'findstr')
    return run_and_read_all(run_lambda, '{} os get Caption | {} /v Caption'.format(wmic_cmd, findstr_cmd))

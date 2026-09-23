def check_compiler_is_gcc(compiler):
    if not IS_LINUX:
        return False

    env = os.environ.copy()
    env['LC_ALL'] = 'C'  # Don't localize output
    try:
        version_string = subprocess.check_output([compiler, '-v'], stderr=subprocess.STDOUT, env=env).decode(*SUBPROCESS_DECODE_ARGS)
    except Exception:
        try:
            version_string = subprocess.check_output([compiler, '--version'], stderr=subprocess.STDOUT, env=env).decode(*SUBPROCESS_DECODE_ARGS)
        except Exception:
            return False
    # Check for 'gcc' or 'g++' for sccache wrapper
    pattern = re.compile("^COLLECT_GCC=(.*)$", re.MULTILINE)
    results = re.findall(pattern, version_string)
    if len(results) != 1:
        return False
    compiler_path = os.path.realpath(results[0].strip())
    # On RHEL/CentOS c++ is a gcc compiler wrapper
    if os.path.basename(compiler_path) == 'c++' and 'gcc version' in version_string:
        return True
    return False

def check_compiler_ok_for_platform(compiler: str) -> bool:
    r'''
    Verifies that the compiler is the expected one for the current platform.

    Args:
        compiler (str): The compiler executable to check.

    Returns:
        True if the compiler is gcc/g++ on Linux or clang/clang++ on macOS,
        and always True for Windows.
    '''
    if IS_WINDOWS:
        return True
    which = subprocess.check_output(['which', compiler], stderr=subprocess.STDOUT)
    # Use os.path.realpath to resolve any symlinks, in particular from 'c++' to e.g. 'g++'.
    compiler_path = os.path.realpath(which.decode(*SUBPROCESS_DECODE_ARGS).strip())
    # Check the compiler name
    if any(name in compiler_path for name in _accepted_compilers_for_platform()):
        return True
    # If ccache is used the compiler path is /usr/bin/ccache. Check by -v flag.
    version_string = subprocess.check_output([compiler, '-v'], stderr=subprocess.STDOUT).decode(*SUBPROCESS_DECODE_ARGS)
    if sys.platform.startswith('linux'):
        # Check for 'gcc' or 'g++'
        pattern = re.compile("^COLLECT_GCC=(.*)$", re.MULTILINE)
        results = re.findall(pattern, version_string)
        if len(results) != 1:
            return False
        compiler_path = os.path.realpath(results[0].strip())
        return any(name in compiler_path for name in _accepted_compilers_for_platform())
    if sys.platform.startswith('darwin'):
        # Check for 'clang' or 'clang++'
        return version_string.startswith("Apple clang")
    return False

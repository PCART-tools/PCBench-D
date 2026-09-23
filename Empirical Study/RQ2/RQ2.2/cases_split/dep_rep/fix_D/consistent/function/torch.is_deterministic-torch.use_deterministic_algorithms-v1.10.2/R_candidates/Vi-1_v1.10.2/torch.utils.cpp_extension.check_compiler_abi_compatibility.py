def check_compiler_abi_compatibility(compiler) -> bool:
    r'''
    Verifies that the given compiler is ABI-compatible with PyTorch.

    Args:
        compiler (str): The compiler executable name to check (e.g. ``g++``).
            Must be executable in a shell process.

    Returns:
        False if the compiler is (likely) ABI-incompatible with PyTorch,
        else True.
    '''
    if not _is_binary_build():
        return True
    if os.environ.get('TORCH_DONT_CHECK_COMPILER_ABI') in ['ON', '1', 'YES', 'TRUE', 'Y']:
        return True

    # First check if the compiler is one of the expected ones for the particular platform.
    if not check_compiler_ok_for_platform(compiler):
        warnings.warn(WRONG_COMPILER_WARNING.format(
            user_compiler=compiler,
            pytorch_compiler=_accepted_compilers_for_platform()[0],
            platform=sys.platform))
        return False

    if sys.platform.startswith('darwin'):
        # There is no particular minimum version we need for clang, so we're good here.
        return True
    try:
        if sys.platform.startswith('linux'):
            minimum_required_version = MINIMUM_GCC_VERSION
            versionstr = subprocess.check_output([compiler, '-dumpfullversion', '-dumpversion'])
            version = versionstr.decode(*SUBPROCESS_DECODE_ARGS).strip().split('.')
        else:
            minimum_required_version = MINIMUM_MSVC_VERSION
            compiler_info = subprocess.check_output(compiler, stderr=subprocess.STDOUT)
            match = re.search(r'(\d+)\.(\d+)\.(\d+)', compiler_info.decode(*SUBPROCESS_DECODE_ARGS).strip())
            version = (0, 0, 0) if match is None else match.groups()
    except Exception:
        _, error, _ = sys.exc_info()
        warnings.warn(f'Error checking compiler version for {compiler}: {error}')
        return False

    if tuple(map(int, version)) >= minimum_required_version:
        return True

    compiler = f'{compiler} {".".join(version)}'
    warnings.warn(ABI_INCOMPATIBILITY_WARNING.format(compiler))

    return False

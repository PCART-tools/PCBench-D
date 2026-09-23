def _overlay_windows_vcvars(env: Dict[str, str]) -> Dict[str, str]:
    vc_arch = 'x64' if IS_64BIT else 'x86'
    vc_env: Dict[str, str] = distutils._msvccompiler._get_vc_env(vc_arch)
    # Keys in `_get_vc_env` are always lowercase.
    # We turn them into uppercase before overlaying vcvars
    # because OS environ keys are always uppercase on Windows.
    # https://stackoverflow.com/a/7797329
    vc_env = {k.upper(): v for k, v in vc_env.items()}
    for k, v in env.items():
        uk = k.upper()
        if uk not in vc_env:
            vc_env[uk] = v
    return vc_env

def _get_vc_env(vc_arch: str) -> dict[str, str]:
    try:
        from setuptools import distutils
        return distutils._msvccompiler._get_vc_env(vc_arch)
    except AttributeError:
        from setuptools._distutils import _msvccompiler
        return _msvccompiler._get_vc_env(vc_arch)

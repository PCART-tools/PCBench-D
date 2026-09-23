def _get_vc_env(vc_arch: str) -> dict[str, str]:
    try:
        from setuptools import distutils  # type: ignore[attr-defined]
        return distutils._msvccompiler._get_vc_env(vc_arch)
    except AttributeError:
        try:
            from setuptools._distutils import _msvccompiler
            return _msvccompiler._get_vc_env(vc_arch)  # type: ignore[attr-defined]
        except AttributeError:
            from setuptools._distutils.compilers.C import msvc
            return msvc._get_vc_env(vc_arch)  # type: ignore[attr-defined]

def _load_global_deps():
    if platform.system() == 'Windows' or sys.executable == 'torch_deploy':
        return

    lib_name = 'libtorch_global_deps' + ('.dylib' if platform.system() == 'Darwin' else '.so')
    here = os.path.abspath(__file__)
    lib_path = os.path.join(os.path.dirname(here), 'lib', lib_name)

    ctypes.CDLL(lib_path, mode=ctypes.RTLD_GLOBAL)

def is_hip_clang() -> bool:
    try:
        hip_path = os.getenv('HIP_PATH', '/opt/rocm/hip')
        with open(hip_path + '/lib/.hipInfo') as f:
            return 'HIP_COMPILER=clang' in f.read()
    except IOError:
        return False

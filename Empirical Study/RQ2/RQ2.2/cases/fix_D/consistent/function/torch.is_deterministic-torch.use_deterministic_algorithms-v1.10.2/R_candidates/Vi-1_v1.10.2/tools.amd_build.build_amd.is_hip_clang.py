def is_hip_clang() -> bool:
    try:
        hip_path = os.getenv('HIP_PATH', '/opt/rocm/hip')
        return 'HIP_COMPILER=clang' in open(hip_path + '/lib/.hipInfo').read()
    except IOError:
        return False

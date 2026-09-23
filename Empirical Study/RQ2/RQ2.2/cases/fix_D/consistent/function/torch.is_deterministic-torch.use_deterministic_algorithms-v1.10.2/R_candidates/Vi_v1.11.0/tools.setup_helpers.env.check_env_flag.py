def check_env_flag(name: str, default: str = '') -> bool:
    return os.getenv(name, default).upper() in ['ON', '1', 'YES', 'TRUE', 'Y']

def check_negative_env_flag(name: str, default: str = '') -> bool:
    return os.getenv(name, default).upper() in ['OFF', '0', 'NO', 'FALSE', 'N']

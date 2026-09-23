def is_sandcastle():
    return os.getenv('SANDCASTLE') == '1' or os.getenv('TW_JOB_USER') == 'sandcastle'

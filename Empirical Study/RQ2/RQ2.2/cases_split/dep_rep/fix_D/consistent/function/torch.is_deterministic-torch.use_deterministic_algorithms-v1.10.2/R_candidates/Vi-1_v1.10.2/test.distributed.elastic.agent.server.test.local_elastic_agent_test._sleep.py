def _sleep(sleep_sec) -> int:
    time.sleep(sleep_sec)
    return int(os.environ["RANK"])

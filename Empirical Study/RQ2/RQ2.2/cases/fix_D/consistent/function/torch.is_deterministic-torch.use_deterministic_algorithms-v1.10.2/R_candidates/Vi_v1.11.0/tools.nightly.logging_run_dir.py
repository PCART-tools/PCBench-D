@functools.lru_cache()
def logging_run_dir() -> str:
    cur_dir = os.path.join(
        logging_base_dir(),
        "{}_{}".format(datetime.datetime.now().strftime(DATETIME_FORMAT), uuid.uuid1()),
    )
    os.makedirs(cur_dir, exist_ok=True)
    return cur_dir

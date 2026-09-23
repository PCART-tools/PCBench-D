def _setup_logger(name: Optional[str] = None):
    log = logging.getLogger(name)
    log.setLevel(os.environ.get("LOGLEVEL", get_log_level()))
    return log

def _setup_logger(name: Optional[str] = None):
    logger = logging.getLogger(name)
    logger.setLevel(os.environ.get("LOGLEVEL", get_log_level()))
    return logger

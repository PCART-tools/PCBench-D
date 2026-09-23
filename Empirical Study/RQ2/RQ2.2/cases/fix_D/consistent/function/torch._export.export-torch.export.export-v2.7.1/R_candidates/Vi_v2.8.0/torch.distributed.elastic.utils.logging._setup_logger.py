def _setup_logger(name: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(os.environ.get("LOGLEVEL", get_log_level()))
    return logger

def log_input(name: str, var: object):
    logging.getLogger("LoggingTensor").info("input", (name,), {}, (var,))

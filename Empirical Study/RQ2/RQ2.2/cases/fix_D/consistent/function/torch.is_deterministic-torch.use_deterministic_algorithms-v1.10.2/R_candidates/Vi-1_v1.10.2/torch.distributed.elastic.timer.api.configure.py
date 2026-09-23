def configure(timer_client: TimerClient):
    """
    Configures a timer client. Must be called before using ``expires``.
    """
    global _timer_client
    _timer_client = timer_client
    logging.info(f"Timer client configured to: {type(_timer_client).__name__}")

  @classmethod
  def wait_for_coordinator(cls, coordinator_address, timeout_secs):
    # The coordinator may not be up before the other hosts try to
    # communicate with it. We check for its existence with retries.
    coordinator_found = False
    max_time = time.time() + timeout_secs
    coordinator_retry_secs = 5
    while not coordinator_found and time.time() < max_time:
      try:
        ip_address = socket.gethostbyname(coordinator_address)
        coordinator_found = True
        logger.debug("Found coordinator with address %s", coordinator_address)
      except socket.gaierror:
        logger.debug(
            "Failed to recognize coordinator address %s"
            " retrying...", coordinator_address
        )
        time.sleep(coordinator_retry_secs)
    if not coordinator_found:
      raise RuntimeError(f"Failed to recognize coordinator address {coordinator_address}")

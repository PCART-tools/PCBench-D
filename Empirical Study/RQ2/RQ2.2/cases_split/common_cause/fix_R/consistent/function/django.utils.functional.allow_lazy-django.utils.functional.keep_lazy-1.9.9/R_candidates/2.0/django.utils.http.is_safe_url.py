def is_safe_url(url, host=None, allowed_hosts=None, require_https=False):
    """
    Return ``True`` if the url is a safe redirection (i.e. it doesn't point to
    a different host and uses a safe scheme).

    Always return ``False`` on an empty url.

    If ``require_https`` is ``True``, only 'https' will be considered a valid
    scheme, as opposed to 'http' and 'https' with the default, ``False``.
    """
    if url is not None:
        url = url.strip()
    if not url:
        return False
    if allowed_hosts is None:
        allowed_hosts = set()
    if host:
        warnings.warn(
            "The host argument is deprecated, use allowed_hosts instead.",
            RemovedInDjango21Warning,
            stacklevel=2,
        )
        # Avoid mutating the passed in allowed_hosts.
        allowed_hosts = allowed_hosts | {host}
    # Chrome treats \ completely as / in paths but it could be part of some
    # basic auth credentials so we need to check both URLs.
    return (_is_safe_url(url, allowed_hosts, require_https=require_https) and
            _is_safe_url(url.replace('\\', '/'), allowed_hosts, require_https=require_https))

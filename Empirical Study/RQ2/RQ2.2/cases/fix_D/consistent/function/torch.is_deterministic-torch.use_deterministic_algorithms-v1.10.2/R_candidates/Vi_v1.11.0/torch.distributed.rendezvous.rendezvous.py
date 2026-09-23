def rendezvous(url: str, rank: int = -1, world_size: int = -1, **kwargs):
    if not isinstance(url, six.string_classes):
        raise RuntimeError("`url` must be a string. {}: {}".format(type(url), url))

    if not isinstance(rank, numbers.Integral):
        raise RuntimeError("`rank` must be an integer. {}".format(rank))

    if not isinstance(world_size, numbers.Integral):
        raise RuntimeError("`world_size` must be an integer. {}".format(world_size))

    # Append node-specific arguments.
    result = urlparse(url)
    if rank != -1 or world_size != -1:
        query_dict: Dict[str, Union[int, str]] = dict(
            pair.split("=") for pair in filter(None, result.query.split("&"))
        )
        assert (
            "rank" not in query_dict and "world_size" not in query_dict
        ), "The url: {url} has node-specific arguments(rank, world_size) already.".format(
            url=url
        )
        if rank != -1:
            query_dict["rank"] = rank
        if world_size != -1:
            query_dict["world_size"] = world_size

        result = result._replace(
            query="{}".format(
                "&".join(["{}={}".format(k, v) for k, v in query_dict.items()])
            )
        )
        url = urlunparse(result)

    if result.scheme not in _rendezvous_handlers:
        raise RuntimeError("No rendezvous handler for {}://".format(result.scheme))
    return _rendezvous_handlers[result.scheme](url, **kwargs)

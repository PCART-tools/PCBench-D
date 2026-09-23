def _raise_not_supported(name: str) -> None:
    raise ValueError("Method ``{}`` not supported for RemoteModule".format(name))

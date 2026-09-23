def load(repo_or_dir, model, *args, source='github', force_reload=False, verbose=True, skip_validation=False,
         **kwargs):
    r"""
    Load a model from a github repo or a local directory.

    Note: Loading a model is the typical use case, but this can also be used to
    for loading other objects such as tokenizers, loss functions, etc.

    If ``source`` is 'github', ``repo_or_dir`` is expected to be
    of the form ``repo_owner/repo_name[:tag_name]`` with an optional
    tag/branch.

    If ``source`` is 'local', ``repo_or_dir`` is expected to be a
    path to a local directory.

    Args:
        repo_or_dir (string): If ``source`` is 'github',
            this should correspond to a github repo with format ``repo_owner/repo_name[:tag_name]`` with
            an optional tag/branch, for example 'pytorch/vision:0.10'. If ``tag_name`` is not specified,
            the default branch is assumed to be ``main`` if it exists, and otherwise ``master``.
            If ``source`` is 'local'  then it should be a path to a local directory.
        model (string): the name of a callable (entrypoint) defined in the
            repo/dir's ``hubconf.py``.
        *args (optional): the corresponding args for callable ``model``.
        source (string, optional): 'github' or 'local'. Specifies how
            ``repo_or_dir`` is to be interpreted. Default is 'github'.
        force_reload (bool, optional): whether to force a fresh download of
            the github repo unconditionally. Does not have any effect if
            ``source = 'local'``. Default is ``False``.
        verbose (bool, optional): If ``False``, mute messages about hitting
            local caches. Note that the message about first download cannot be
            muted. Does not have any effect if ``source = 'local'``.
            Default is ``True``.
        skip_validation (bool, optional): if ``False``, torchhub will check that the branch or commit
            specified by the ``github`` argument properly belongs to the repo owner. This will make
            requests to the GitHub API; you can specify a non-default GitHub token by setting the
            ``GITHUB_TOKEN`` environment variable. Default is ``False``.
        **kwargs (optional): the corresponding kwargs for callable ``model``.

    Returns:
        The output of the ``model`` callable when called with the given
        ``*args`` and ``**kwargs``.

    Example:
        >>> # from a github repo
        >>> repo = 'pytorch/vision'
        >>> model = torch.hub.load(repo, 'resnet50', pretrained=True)
        >>> # from a local directory
        >>> path = '/some/local/path/pytorch/vision'
        >>> model = torch.hub.load(path, 'resnet50', pretrained=True)
    """
    source = source.lower()

    if source not in ('github', 'local'):
        raise ValueError(
            f'Unknown source: "{source}". Allowed values: "github" | "local".')

    if source == 'github':
        repo_or_dir = _get_cache_or_reload(repo_or_dir, force_reload, verbose, skip_validation)

    model = _load_local(repo_or_dir, model, *args, **kwargs)
    return model

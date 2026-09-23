def list(github, force_reload=False, skip_validation=False):
    r"""
    List all callable entrypoints available in the repo specified by ``github``.

    Args:
        github (string): a string with format "repo_owner/repo_name[:tag_name]" with an optional
            tag/branch. If ``tag_name`` is not specified, the default branch is assumed to be ``main`` if
            it exists, and otherwise ``master``.
            Example: 'pytorch/vision:0.10'
        force_reload (bool, optional): whether to discard the existing cache and force a fresh download.
            Default is ``False``.
        skip_validation (bool, optional): if ``False``, torchhub will check that the branch or commit
            specified by the ``github`` argument properly belongs to the repo owner. This will make
            requests to the GitHub API; you can specify a non-default GitHub token by setting the
            ``GITHUB_TOKEN`` environment variable. Default is ``False``.
    Returns:
        list: The available callables entrypoint

    Example:
        >>> entrypoints = torch.hub.list('pytorch/vision', force_reload=True)
    """
    repo_dir = _get_cache_or_reload(github, force_reload, verbose=True, skip_validation=skip_validation)

    sys.path.insert(0, repo_dir)

    hubconf_path = os.path.join(repo_dir, MODULE_HUBCONF)
    hub_module = import_module(MODULE_HUBCONF, hubconf_path)

    sys.path.remove(repo_dir)

    # We take functions starts with '_' as internal helper functions
    entrypoints = [f for f in dir(hub_module) if callable(getattr(hub_module, f)) and not f.startswith('_')]

    return entrypoints

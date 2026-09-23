def help(github, model, force_reload=False, skip_validation=False):
    r"""
    Show the docstring of entrypoint ``model``.

    Args:
        github (string): a string with format <repo_owner/repo_name[:tag_name]> with an optional
            tag/branch. If ``tag_name`` is not specified, the default branch is assumed to be ``main`` if
            it exists, and otherwise ``master``.
            Example: 'pytorch/vision:0.10'
        model (string): a string of entrypoint name defined in repo's ``hubconf.py``
        force_reload (bool, optional): whether to discard the existing cache and force a fresh download.
            Default is ``False``.
        skip_validation (bool, optional): if ``False``, torchhub will check that the branch or commit
            specified by the ``github`` argument properly belongs to the repo owner. This will make
            requests to the GitHub API; you can specify a non-default GitHub token by setting the
            ``GITHUB_TOKEN`` environment variable. Default is ``False``.
    Example:
        >>> print(torch.hub.help('pytorch/vision', 'resnet18', force_reload=True))
    """
    repo_dir = _get_cache_or_reload(github, force_reload, verbose=True, skip_validation=skip_validation)

    sys.path.insert(0, repo_dir)

    hubconf_path = os.path.join(repo_dir, MODULE_HUBCONF)
    hub_module = _import_module(MODULE_HUBCONF, hubconf_path)

    sys.path.remove(repo_dir)

    entry = _load_entry_from_hubconf(hub_module, model)

    return entry.__doc__

def get_config():
    """Create, populate and return the VersioneerConfig() object."""
    # these strings are filled in when 'setup.py versioneer' creates
    # _version.py
    cfg = VersioneerConfig()
    cfg.VCS = "git"
    cfg.style = "pep440"
    cfg.tag_prefix = ""
    cfg.parentdir_prefix = "dask-"
    cfg.versionfile_source = "dask/_version.py"
    cfg.verbose = False
    return cfg

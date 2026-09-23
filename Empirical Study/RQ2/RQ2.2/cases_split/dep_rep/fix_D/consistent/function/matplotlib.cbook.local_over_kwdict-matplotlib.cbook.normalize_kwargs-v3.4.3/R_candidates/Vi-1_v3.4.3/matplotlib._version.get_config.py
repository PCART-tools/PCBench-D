def get_config():
    # these strings are filled in when 'setup.py versioneer' creates
    # _version.py
    cfg = VersioneerConfig()
    cfg.VCS = "git"
    cfg.style = "pep440-post"
    cfg.tag_prefix = "v"
    cfg.parentdir_prefix = "matplotlib-"
    cfg.versionfile_source = "lib/matplotlib/_version.py"
    cfg.verbose = False
    return cfg

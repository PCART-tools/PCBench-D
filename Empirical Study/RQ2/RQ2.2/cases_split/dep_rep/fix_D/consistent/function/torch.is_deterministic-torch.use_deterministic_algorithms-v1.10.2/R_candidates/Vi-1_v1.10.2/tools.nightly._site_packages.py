def _site_packages(dirname: str, platform: str) -> str:
    if platform.startswith("win"):
        template = os.path.join(dirname, "Lib", "site-packages")
    else:
        template = os.path.join(dirname, "lib", "python*.*", "site-packages")
    spdir = glob.glob(template)[0]
    return spdir

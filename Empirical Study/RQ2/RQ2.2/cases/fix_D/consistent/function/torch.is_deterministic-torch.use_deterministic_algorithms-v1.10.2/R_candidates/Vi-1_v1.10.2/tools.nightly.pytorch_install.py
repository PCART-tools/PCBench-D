@timed("Installing pytorch nightly binaries")
def pytorch_install(url: str) -> "tempfile.TemporaryDirectory[str]":
    """"Install pytorch into a temporary directory"""
    pytdir = tempfile.TemporaryDirectory()
    cmd = ["conda", "create", "--yes", "--no-deps", "--prefix", pytdir.name, url]
    p = subprocess.run(cmd, check=True)
    return pytdir

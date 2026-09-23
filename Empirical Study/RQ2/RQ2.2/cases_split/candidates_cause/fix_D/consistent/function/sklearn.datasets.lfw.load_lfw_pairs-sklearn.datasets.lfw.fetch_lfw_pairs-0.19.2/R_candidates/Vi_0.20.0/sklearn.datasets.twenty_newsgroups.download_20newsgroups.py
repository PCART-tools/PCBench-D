@deprecated("Function 'download_20newsgroups' was renamed to "
            "'_download_20newsgroups' in version 0.20 and will be removed in "
            "release 0.22.")
def download_20newsgroups(target_dir, cache_path):
    return _download_20newsgroups(target_dir, cache_path)

def looks_like_git_sha(tag):
    """Returns a boolean to check if a tag looks like a git sha

    For reference a sha1 is 40 characters with only 0-9a-f and contains no
    "-" characters
    """
    return re.match(SHA_PATTERN, tag) is not None

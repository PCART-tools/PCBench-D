def _accept(prefix):
    # Magic number was taken from https://en.wikipedia.org/wiki/JPEG
    return prefix[0:3] == b"\xFF\xD8\xFF"

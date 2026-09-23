def _accept(prefix):
    return prefix.lstrip()[:7] == b"#define"

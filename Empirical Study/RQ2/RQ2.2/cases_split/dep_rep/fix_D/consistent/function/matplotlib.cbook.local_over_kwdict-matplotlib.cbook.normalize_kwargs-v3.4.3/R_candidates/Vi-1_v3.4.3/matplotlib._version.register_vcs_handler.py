def register_vcs_handler(vcs, method):  # decorator
    def decorate(f):
        if vcs not in HANDLERS:
            HANDLERS[vcs] = {}
        HANDLERS[vcs][method] = f
        return f
    return decorate

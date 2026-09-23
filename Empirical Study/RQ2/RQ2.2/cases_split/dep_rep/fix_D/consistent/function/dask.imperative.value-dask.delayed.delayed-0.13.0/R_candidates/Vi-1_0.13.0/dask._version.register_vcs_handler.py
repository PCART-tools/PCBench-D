def register_vcs_handler(vcs, method):  # decorator
    """Decorator to mark a method as the handler for a particular VCS."""
    def decorate(f):
        """Store f in HANDLERS[vcs][method]."""
        if vcs not in HANDLERS:
            HANDLERS[vcs] = {}
        HANDLERS[vcs][method] = f
        return f
    return decorate

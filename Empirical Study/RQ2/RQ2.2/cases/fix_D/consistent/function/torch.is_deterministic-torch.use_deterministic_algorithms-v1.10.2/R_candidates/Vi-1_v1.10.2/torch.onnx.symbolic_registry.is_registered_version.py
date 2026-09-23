def is_registered_version(domain, version):
    global _registry
    return (domain, version) in _registry

def unsupported(func):
    def wrapper(self):
        return func(self)

    wrapper.is_supported = False
    return wrapper

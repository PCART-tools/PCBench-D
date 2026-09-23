    @wraps(np.clip)
    def clip(self, min=None, max=None):
        from .ufunc import clip
        return clip(self, min, max)

    @docstring.dedent_interpd
    def annotate(self, *args, **kwargs):
        a = mtext.Annotation(*args, **kwargs)
        a.set_transform(mtransforms.IdentityTransform())
        if 'clip_on' in kwargs:
            a.set_clip_path(self.patch)
        self._add_text(a)
        return a

    def _repr_latex_(self):
        """
        Returns a LaTeX representation for a particular object.
        Mainly for use with nbconvert (jupyter notebook conversion to pdf).
        """
        if config.get_option('display.latex.repr'):
            return self.to_latex()
        else:
            return None

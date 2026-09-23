class FontEntry:
    """
    A class for storing Font properties.  It is used when populating
    the font lookup dictionary.
    """
    def __init__(self,
                 fname  ='',
                 name   ='',
                 style  ='normal',
                 variant='normal',
                 weight ='normal',
                 stretch='normal',
                 size   ='medium',
                 ):
        self.fname   = fname
        self.name    = name
        self.style   = style
        self.variant = variant
        self.weight  = weight
        self.stretch = stretch
        try:
            self.size = str(float(size))
        except ValueError:
            self.size = size

    def __repr__(self):
        return "<Font '%s' (%s) %s %s %s %s>" % (
            self.name, os.path.basename(self.fname), self.style, self.variant,
            self.weight, self.stretch)

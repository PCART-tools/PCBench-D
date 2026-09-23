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

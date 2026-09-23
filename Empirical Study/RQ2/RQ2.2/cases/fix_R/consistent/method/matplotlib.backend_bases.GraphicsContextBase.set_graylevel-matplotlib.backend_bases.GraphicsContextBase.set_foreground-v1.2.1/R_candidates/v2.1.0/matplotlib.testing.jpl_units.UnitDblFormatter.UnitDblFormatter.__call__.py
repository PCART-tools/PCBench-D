   def __call__( self, x, pos = None ):
      'Return the format for tick val x at position pos'
      if len(self.locs) == 0:
         return ''
      else:
         return str(x)

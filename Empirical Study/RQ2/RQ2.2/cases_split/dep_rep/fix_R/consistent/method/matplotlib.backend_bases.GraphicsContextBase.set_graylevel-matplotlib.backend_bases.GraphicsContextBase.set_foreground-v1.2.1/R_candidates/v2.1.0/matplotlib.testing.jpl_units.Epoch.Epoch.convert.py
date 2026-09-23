   def convert( self, frame ):
      if self._frame == frame:
         return self

      offset = self.allowed[ self._frame ][ frame ]

      return Epoch( frame, self._seconds + offset, self._jd )

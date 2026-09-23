   def secondsPast( self, frame, jd ):
      t = self
      if frame != self._frame:
         t = self.convert( frame )

      delta = t._jd - jd
      return t._seconds + delta * 86400

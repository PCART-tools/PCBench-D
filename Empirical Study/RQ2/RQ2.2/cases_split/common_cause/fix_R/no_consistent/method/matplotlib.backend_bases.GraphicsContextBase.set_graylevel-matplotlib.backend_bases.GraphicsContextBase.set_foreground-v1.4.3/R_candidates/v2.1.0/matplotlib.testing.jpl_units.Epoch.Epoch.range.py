   def range( start, stop, step ):
      """Generate a range of Epoch objects.

      Similar to the Python range() method.  Returns the range [
      start, stop ) at the requested step.  Each element will be a
      Epoch object.

      = INPUT VARIABLES
      - start    The starting value of the range.
      - stop     The stop value of the range.
      - step     Step to use.

      = RETURN VALUE
      - Returns a list contianing the requested Epoch values.
      """
      elems = []

      i = 0
      while True:
         d = start + i * step
         if d >= stop:
            break

         elems.append( d )
         i += 1

      return elems

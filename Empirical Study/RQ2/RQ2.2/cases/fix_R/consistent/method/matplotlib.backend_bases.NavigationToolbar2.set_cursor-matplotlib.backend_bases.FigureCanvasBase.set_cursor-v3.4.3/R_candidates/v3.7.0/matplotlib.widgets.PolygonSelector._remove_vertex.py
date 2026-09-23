    def _remove_vertex(self, i):
        """Remove vertex with index i."""
        if (len(self._xys) > 2 and
                self._selection_completed and
                i in (0, len(self._xys) - 1)):
            # If selecting the first or final vertex, remove both first and
            # last vertex as they are the same for a closed polygon
            self._xys.pop(0)
            self._xys.pop(-1)
            # Close the polygon again by appending the new first vertex to the
            # end
            self._xys.append(self._xys[0])
        else:
            self._xys.pop(i)
        if len(self._xys) <= 2:
            # If only one point left, return to incomplete state to let user
            # start drawing again
            self._selection_completed = False
            self._remove_box()

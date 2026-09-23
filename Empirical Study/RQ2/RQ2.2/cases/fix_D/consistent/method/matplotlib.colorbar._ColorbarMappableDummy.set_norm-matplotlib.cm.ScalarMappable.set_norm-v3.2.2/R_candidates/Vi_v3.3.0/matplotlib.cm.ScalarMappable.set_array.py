    def set_array(self, A):
        """
        Set the image array from numpy array *A*.

        Parameters
        ----------
        A : ndarray
        """
        self._A = A
        self._update_dict['array'] = True

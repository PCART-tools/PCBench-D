    def set_array(self, A):
        """Set the image array from numpy array *A*.

        Parameters
        ----------
        A : ndarray
        """
        self._A = A
        self.update_dict['array'] = True

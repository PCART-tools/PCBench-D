    def get_indices(self):
        a = [i for i in range(len(self._axis_var)) if self._axis_var[i].get()]
        return a

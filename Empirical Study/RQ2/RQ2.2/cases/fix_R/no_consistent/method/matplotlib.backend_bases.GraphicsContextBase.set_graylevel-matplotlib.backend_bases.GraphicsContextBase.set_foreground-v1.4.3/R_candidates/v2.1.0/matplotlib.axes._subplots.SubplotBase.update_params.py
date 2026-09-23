    def update_params(self):
        """update the subplot position from fig.subplotpars"""

        self.figbox, self.rowNum, self.colNum, self.numRows, self.numCols = \
            self.get_subplotspec().get_position(self.figure,
                                                return_all=True)

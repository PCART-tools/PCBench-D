    def __init__(self, df, na_rep='', float_format=None, cols=None,
                 header=True, index=True, index_label=None, merge_cells=False,
                 inf_rep='inf'):
        self.df = df
        self.rowcounter = 0
        self.na_rep = na_rep
        self.columns = cols
        if cols is None:
            self.columns = df.columns
        self.float_format = float_format
        self.index = index
        self.index_label = index_label
        self.header = header
        self.merge_cells = merge_cells
        self.inf_rep = inf_rep

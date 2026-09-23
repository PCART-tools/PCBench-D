    def __init__(self, tol, remove_text, savefig_kwargs):
        self.func = self.baseline_dir = self.result_dir = None
        self.tol = tol
        self.remove_text = remove_text
        self.savefig_kwargs = savefig_kwargs

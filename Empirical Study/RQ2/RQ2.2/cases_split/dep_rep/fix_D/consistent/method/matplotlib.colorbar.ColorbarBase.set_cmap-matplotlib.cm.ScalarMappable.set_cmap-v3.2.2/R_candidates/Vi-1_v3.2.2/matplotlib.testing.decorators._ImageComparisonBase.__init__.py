    def __init__(self, func, tol, remove_text, savefig_kwargs):
        self.func = func
        self.baseline_dir, self.result_dir = _image_directories(func)
        self.tol = tol
        self.remove_text = remove_text
        self.savefig_kwargs = savefig_kwargs

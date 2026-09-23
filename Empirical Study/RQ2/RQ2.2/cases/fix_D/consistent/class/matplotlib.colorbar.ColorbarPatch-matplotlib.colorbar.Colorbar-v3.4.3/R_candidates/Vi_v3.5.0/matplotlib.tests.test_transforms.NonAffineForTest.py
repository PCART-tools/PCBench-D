class NonAffineForTest(mtransforms.Transform):
    """
    A class which looks like a non affine transform, but does whatever
    the given transform does (even if it is affine). This is very useful
    for testing NonAffine behaviour with a simple Affine transform.

    """
    is_affine = False
    output_dims = 2
    input_dims = 2

    def __init__(self, real_trans, *args, **kwargs):
        self.real_trans = real_trans
        super().__init__(*args, **kwargs)

    def transform_non_affine(self, values):
        return self.real_trans.transform(values)

    def transform_path_non_affine(self, path):
        return self.real_trans.transform_path(path)

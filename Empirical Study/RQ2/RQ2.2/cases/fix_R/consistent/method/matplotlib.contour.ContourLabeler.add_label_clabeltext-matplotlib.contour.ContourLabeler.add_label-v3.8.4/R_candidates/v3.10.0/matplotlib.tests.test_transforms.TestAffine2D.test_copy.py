    def test_copy(self):
        a = mtransforms.Affine2D()
        b = mtransforms.Affine2D()
        s = a + b
        # Updating a dependee should invalidate a copy of the dependent.
        s.get_matrix()  # resolve it.
        s1 = copy.copy(s)
        assert not s._invalid and not s1._invalid
        a.translate(1, 2)
        assert s._invalid and s1._invalid
        assert (s1.get_matrix() == a.get_matrix()).all()
        # Updating a copy of a dependee shouldn't invalidate a dependent.
        s.get_matrix()  # resolve it.
        b1 = copy.copy(b)
        b1.translate(3, 4)
        assert not s._invalid
        assert_array_equal(s.get_matrix(), a.get_matrix())

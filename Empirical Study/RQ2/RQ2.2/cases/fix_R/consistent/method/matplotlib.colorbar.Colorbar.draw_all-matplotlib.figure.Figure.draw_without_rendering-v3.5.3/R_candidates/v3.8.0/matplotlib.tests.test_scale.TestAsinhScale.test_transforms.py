    def test_transforms(self):
        a0 = 17.0
        a = np.linspace(-50, 50, 100)

        forward = AsinhTransform(a0)
        inverse = forward.inverted()
        invinv = inverse.inverted()

        a_forward = forward.transform_non_affine(a)
        a_inverted = inverse.transform_non_affine(a_forward)
        assert_allclose(a_inverted, a)

        a_invinv = invinv.transform_non_affine(a)
        assert_allclose(a_invinv, a0 * np.arcsinh(a / a0))

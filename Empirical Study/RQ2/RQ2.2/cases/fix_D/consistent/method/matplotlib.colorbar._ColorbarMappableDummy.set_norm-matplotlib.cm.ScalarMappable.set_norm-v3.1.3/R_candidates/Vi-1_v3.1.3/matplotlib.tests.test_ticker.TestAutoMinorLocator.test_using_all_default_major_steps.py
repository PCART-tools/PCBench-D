    def test_using_all_default_major_steps(self):
        with matplotlib.rc_context({'_internal.classic_mode': False}):
            majorsteps = [x[0] for x in self.majorstep_minordivisions]
            assert np.allclose(majorsteps, mticker.AutoLocator()._steps)

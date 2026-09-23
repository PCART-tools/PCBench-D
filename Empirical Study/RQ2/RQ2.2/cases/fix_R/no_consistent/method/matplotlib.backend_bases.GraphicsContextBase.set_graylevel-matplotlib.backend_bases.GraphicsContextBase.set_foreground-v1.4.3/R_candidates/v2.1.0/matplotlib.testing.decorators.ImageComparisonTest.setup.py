    def setup(self):
        func = self.func
        plt.close('all')
        self.setup_class()
        try:
            matplotlib.style.use(self.style)
            matplotlib.testing.set_font_settings_for_testing()
            func()
            assert len(plt.get_fignums()) == len(self.baseline_images), (
                "Test generated {} images but there are {} baseline images"
                .format(len(plt.get_fignums()), len(self.baseline_images)))
        except:
            # Restore original settings before raising errors.
            self.teardown_class()
            raise

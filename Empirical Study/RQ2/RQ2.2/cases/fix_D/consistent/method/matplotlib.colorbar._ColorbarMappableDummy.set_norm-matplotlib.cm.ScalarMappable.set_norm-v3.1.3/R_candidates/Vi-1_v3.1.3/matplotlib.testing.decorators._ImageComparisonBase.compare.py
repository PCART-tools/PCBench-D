    def compare(self, idx, baseline, extension):
        __tracebackhide__ = True
        fignum = plt.get_fignums()[idx]
        fig = plt.figure(fignum)

        if self.remove_text:
            remove_ticks_and_titles(fig)

        actual_fname = (
            os.path.join(self.result_dir, baseline) + '.' + extension)
        kwargs = self.savefig_kwargs.copy()
        if extension == 'pdf':
            kwargs.setdefault('metadata',
                              {'Creator': None, 'Producer': None,
                               'CreationDate': None})
        fig.savefig(actual_fname, **kwargs)

        expected_fname = self.copy_baseline(baseline, extension)
        _raise_on_image_difference(expected_fname, actual_fname, self.tol)

    def compare(self, idx, baseline, extension, *, _lock=False):
        __tracebackhide__ = True
        fignum = plt.get_fignums()[idx]
        fig = plt.figure(fignum)

        if self.remove_text:
            remove_ticks_and_titles(fig)

        actual_path = (self.result_dir / baseline).with_suffix(f'.{extension}')
        kwargs = self.savefig_kwargs.copy()
        if extension == 'pdf':
            kwargs.setdefault('metadata',
                              {'Creator': None, 'Producer': None,
                               'CreationDate': None})

        lock = cbook._lock_path(actual_path) if _lock else nullcontext()
        with lock:
            fig.savefig(actual_path, **kwargs)
            expected_path = self.copy_baseline(baseline, extension)
            _raise_on_image_difference(expected_path, actual_path, self.tol)

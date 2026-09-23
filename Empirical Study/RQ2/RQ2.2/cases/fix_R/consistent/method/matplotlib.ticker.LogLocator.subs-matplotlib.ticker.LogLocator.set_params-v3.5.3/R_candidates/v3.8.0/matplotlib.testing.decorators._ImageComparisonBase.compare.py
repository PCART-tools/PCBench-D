    def compare(self, fig, baseline, extension, *, _lock=False):
        __tracebackhide__ = True

        if self.remove_text:
            remove_ticks_and_titles(fig)

        actual_path = (self.result_dir / baseline).with_suffix(f'.{extension}')
        kwargs = self.savefig_kwargs.copy()
        if extension == 'pdf':
            kwargs.setdefault('metadata',
                              {'Creator': None, 'Producer': None,
                               'CreationDate': None})

        lock = (cbook._lock_path(actual_path)
                if _lock else contextlib.nullcontext())
        with lock:
            try:
                fig.savefig(actual_path, **kwargs)
            finally:
                # Matplotlib has an autouse fixture to close figures, but this
                # makes things more convenient for third-party users.
                plt.close(fig)
            expected_path = self.copy_baseline(baseline, extension)
            _raise_on_image_difference(expected_path, actual_path, self.tol)

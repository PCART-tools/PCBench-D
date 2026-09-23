    def copy_baseline(self, baseline, extension):
        baseline_path = self.baseline_dir / baseline
        orig_expected_path = baseline_path.with_suffix(f'.{extension}')
        if extension == 'eps' and not orig_expected_path.exists():
            orig_expected_path = orig_expected_path.with_suffix('.pdf')
        expected_fname = make_test_filename(
            self.result_dir / orig_expected_path.name, 'expected')
        try:
            # os.symlink errors if the target already exists.
            with contextlib.suppress(OSError):
                os.remove(expected_fname)
            try:
                os.symlink(orig_expected_path, expected_fname)
            except OSError:  # On Windows, symlink *may* be unavailable.
                shutil.copyfile(orig_expected_path, expected_fname)
        except OSError as err:
            raise ImageComparisonFailure(
                f"Missing baseline image {expected_fname} because the "
                f"following file cannot be accessed: "
                f"{orig_expected_path}") from err
        return expected_fname

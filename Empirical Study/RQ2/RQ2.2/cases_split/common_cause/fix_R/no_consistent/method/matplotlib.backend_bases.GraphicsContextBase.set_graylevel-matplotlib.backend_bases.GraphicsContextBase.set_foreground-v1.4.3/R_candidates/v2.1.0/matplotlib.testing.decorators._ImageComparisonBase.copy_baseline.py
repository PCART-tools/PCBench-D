    def copy_baseline(self, baseline, extension):
        baseline_path = os.path.join(self.baseline_dir, baseline)
        orig_expected_fname = baseline_path + '.' + extension
        if extension == 'eps' and not os.path.exists(orig_expected_fname):
            orig_expected_fname = baseline_path + '.pdf'
        expected_fname = make_test_filename(os.path.join(
            self.result_dir, os.path.basename(orig_expected_fname)), 'expected')
        if os.path.exists(orig_expected_fname):
            shutil.copyfile(orig_expected_fname, expected_fname)
        else:
            reason = ("Do not have baseline image {0} because this "
                      "file does not exist: {1}".format(expected_fname,
                                                        orig_expected_fname))
            raise ImageComparisonFailure(reason)
        return expected_fname

    def test_use_locale(self):
        conv = locale.localeconv()
        sep = conv['thousands_sep']
        if not sep or conv['grouping'][-1:] in ([], [locale.CHAR_MAX]):
            pytest.skip('Locale does not apply grouping')  # pragma: no cover

        with mpl.rc_context({'axes.formatter.use_locale': True}):
            tmp_form = mticker.ScalarFormatter()
            assert tmp_form.get_useLocale()

            tmp_form.create_dummy_axis()
            tmp_form.set_bounds(0, 10)
            tmp_form.set_locs([1, 2, 3])
            assert sep in tmp_form(1e9)

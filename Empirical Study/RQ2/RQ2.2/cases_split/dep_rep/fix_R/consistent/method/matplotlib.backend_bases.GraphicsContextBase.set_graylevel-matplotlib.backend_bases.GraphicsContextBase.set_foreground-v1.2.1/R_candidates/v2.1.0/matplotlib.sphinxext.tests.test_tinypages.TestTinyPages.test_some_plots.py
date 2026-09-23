    def test_some_plots(self):
        assert isdir(self.html_dir)

        def plot_file(num):
            return pjoin(self.html_dir, 'some_plots-{0}.png'.format(num))

        range_10, range_6, range_4 = [plot_file(i) for i in range(1, 4)]
        # Plot 5 is range(6) plot
        assert filecmp.cmp(range_6, plot_file(5))
        # Plot 7 is range(4) plot
        assert filecmp.cmp(range_4, plot_file(7))
        # Plot 11 is range(10) plot
        assert filecmp.cmp(range_10, plot_file(11))
        # Plot 12 uses the old range(10) figure and the new range(6) figure
        assert filecmp.cmp(range_10, plot_file('12_00'))
        assert filecmp.cmp(range_6, plot_file('12_01'))
        # Plot 13 shows close-figs in action
        assert filecmp.cmp(range_4, plot_file(13))
        # Plot 14 has included source
        with open(pjoin(self.html_dir, 'some_plots.html'), 'rb') as fobj:
            html_contents = fobj.read()
        assert b'# Only a comment' in html_contents
        # check plot defined in external file.
        assert filecmp.cmp(range_4, pjoin(self.html_dir, 'range4.png'))
        assert filecmp.cmp(range_6, pjoin(self.html_dir, 'range6.png'))
        # check if figure caption made it into html file
        assert b'This is the caption for plot 15.' in html_contents

    @pytest.mark.parametrize('left, right, offset', offset_data)
    def test_offset_value(self, left, right, offset):
        fig, ax = plt.subplots()
        formatter = ax.get_xaxis().get_major_formatter()

        with warnings.catch_warnings(record=True) as w:
            warnings.filterwarnings('always', 'Attempting to set identical',
                                    UserWarning)
            ax.set_xlim(left, right)
        assert len(w) == (1 if left == right else 0)
        ax.get_xaxis()._update_ticks()
        assert formatter.offset == offset

        with warnings.catch_warnings(record=True) as w:
            warnings.filterwarnings('always', 'Attempting to set identical',
                                    UserWarning)
            ax.set_xlim(right, left)
        assert len(w) == (1 if left == right else 0)
        ax.get_xaxis()._update_ticks()
        assert formatter.offset == offset

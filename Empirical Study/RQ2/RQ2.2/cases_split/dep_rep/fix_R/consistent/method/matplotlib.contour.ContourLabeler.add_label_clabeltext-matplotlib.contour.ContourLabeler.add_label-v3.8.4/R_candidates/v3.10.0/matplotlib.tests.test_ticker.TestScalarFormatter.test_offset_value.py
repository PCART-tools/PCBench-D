    @pytest.mark.parametrize('left, right, offset', offset_data)
    def test_offset_value(self, left, right, offset):
        fig, ax = plt.subplots()
        formatter = ax.xaxis.get_major_formatter()

        with (pytest.warns(UserWarning, match='Attempting to set identical')
              if left == right else nullcontext()):
            ax.set_xlim(left, right)
        ax.xaxis._update_ticks()
        assert formatter.offset == offset

        with (pytest.warns(UserWarning, match='Attempting to set identical')
              if left == right else nullcontext()):
            ax.set_xlim(right, left)
        ax.xaxis._update_ticks()
        assert formatter.offset == offset

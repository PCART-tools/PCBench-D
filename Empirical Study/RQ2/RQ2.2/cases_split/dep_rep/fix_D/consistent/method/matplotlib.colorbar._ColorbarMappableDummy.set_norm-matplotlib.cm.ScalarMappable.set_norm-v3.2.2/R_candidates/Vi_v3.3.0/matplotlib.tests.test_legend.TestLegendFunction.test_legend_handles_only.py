    def test_legend_handles_only(self):
        lines = plt.plot(range(10))
        with pytest.raises(TypeError, match='but found an Artist'):
            # a single arg is interpreted as labels
            # it's a common error to just pass handles
            plt.legend(lines)

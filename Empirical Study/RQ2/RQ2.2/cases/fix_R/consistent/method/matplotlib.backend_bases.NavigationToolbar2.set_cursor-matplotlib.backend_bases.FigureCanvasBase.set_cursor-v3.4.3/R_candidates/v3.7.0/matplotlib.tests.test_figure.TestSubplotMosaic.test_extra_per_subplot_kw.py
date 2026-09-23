    def test_extra_per_subplot_kw(self):
        with pytest.raises(
                ValueError, match=f'The keys {set("B")!r} are in'
        ):
            Figure().subplot_mosaic("A", per_subplot_kw={"B": {}})

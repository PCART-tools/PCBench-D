    @pytest.mark.parametrize("fdata", fdata, ids=fids)
    def test_non_string_fails(self, fdata):
        with pytest.raises(TypeError):
            cat.UnitData(fdata)

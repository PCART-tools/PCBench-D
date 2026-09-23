def test_stash_not_pop():
    @skippable(stash=["foo"])
    class Layer1(nn.Module):
        pass

    with pytest.raises(TypeError) as e:
        verify_skippables(nn.Sequential(Layer1()))
    assert "no module declared 'foo' as poppable but stashed" in str(e.value)

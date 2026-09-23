def test_pop_unknown():
    @skippable(pop=["foo"])
    class Layer1(nn.Module):
        pass

    with pytest.raises(TypeError) as e:
        verify_skippables(nn.Sequential(Layer1()))
    assert "'0' declared 'foo' as poppable but it was not stashed" in str(e.value)

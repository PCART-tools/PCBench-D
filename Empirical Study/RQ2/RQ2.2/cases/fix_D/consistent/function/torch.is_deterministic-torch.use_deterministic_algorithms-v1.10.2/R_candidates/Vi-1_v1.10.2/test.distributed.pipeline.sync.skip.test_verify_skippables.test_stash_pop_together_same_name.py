def test_stash_pop_together_same_name():
    @skippable(stash=["foo"], pop=["foo"])
    class Layer1(nn.Module):
        pass

    with pytest.raises(TypeError) as e:
        verify_skippables(nn.Sequential(Layer1()))
    assert "'0' declared 'foo' both as stashable and as poppable" in str(e.value)

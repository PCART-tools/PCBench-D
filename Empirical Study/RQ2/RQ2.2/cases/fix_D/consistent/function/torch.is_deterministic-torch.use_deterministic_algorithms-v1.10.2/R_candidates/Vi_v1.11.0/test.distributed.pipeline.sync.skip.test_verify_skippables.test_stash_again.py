def test_stash_again():
    @skippable(stash=["foo"])
    class Layer1(nn.Module):
        pass

    @skippable(stash=["foo"])
    class Layer2(nn.Module):
        pass

    @skippable(pop=["foo"])
    class Layer3(nn.Module):
        pass

    with pytest.raises(TypeError) as e:
        verify_skippables(nn.Sequential(Layer1(), Layer2(), Layer3()))
    assert "'1' redeclared 'foo' as stashable" in str(e.value)

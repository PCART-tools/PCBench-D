def test_pop_again():
    @skippable(stash=["foo"])
    class Layer1(nn.Module):
        pass

    @skippable(pop=["foo"])
    class Layer2(nn.Module):
        pass

    @skippable(pop=["foo"])
    class Layer3(nn.Module):
        pass

    with pytest.raises(TypeError) as e:
        verify_skippables(nn.Sequential(Layer1(), Layer2(), Layer3()))
    assert "'2' redeclared 'foo' as poppable" in str(e.value)

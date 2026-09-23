def test_double_stash_pop():
    @skippable(stash=["foo"])
    class Layer1(nn.Module):
        pass

    @skippable(pop=["foo"])
    class Layer2(nn.Module):
        pass

    @skippable(stash=["foo"])
    class Layer3(nn.Module):
        pass

    @skippable(pop=["foo"])
    class Layer4(nn.Module):
        pass

    with pytest.raises(TypeError) as e:
        verify_skippables(nn.Sequential(Layer1(), Layer2(), Layer3(), Layer4()))
    assert "'2' redeclared 'foo' as stashable" in str(e.value)
    assert "'3' redeclared 'foo' as poppable" in str(e.value)

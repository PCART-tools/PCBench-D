def test_stash_pop_together_different_names():
    @skippable(stash=["foo"])
    class Layer1(nn.Module):
        pass

    @skippable(pop=["foo"], stash=["bar"])
    class Layer2(nn.Module):
        pass

    @skippable(pop=["bar"])
    class Layer3(nn.Module):
        pass

    verify_skippables(nn.Sequential(Layer1(), Layer2(), Layer3()))

def test_matching():
    @skippable(stash=["foo"])
    class Layer1(nn.Module):
        pass

    @skippable(pop=["foo"])
    class Layer2(nn.Module):
        pass

    verify_skippables(nn.Sequential(Layer1(), Layer2()))

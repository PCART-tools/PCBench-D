def test_double_stash_pop_but_isolated():
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

    ns1 = Namespace()
    ns2 = Namespace()

    verify_skippables(
        nn.Sequential(Layer1().isolate(ns1), Layer2().isolate(ns1), Layer3().isolate(ns2), Layer4().isolate(ns2),)
    )

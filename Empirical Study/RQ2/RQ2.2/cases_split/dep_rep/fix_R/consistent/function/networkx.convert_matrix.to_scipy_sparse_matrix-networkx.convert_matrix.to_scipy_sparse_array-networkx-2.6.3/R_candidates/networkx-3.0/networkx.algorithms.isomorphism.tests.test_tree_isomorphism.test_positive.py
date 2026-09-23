def test_positive(maxk=14):

    print("positive test")

    for k in range(2, maxk + 1):
        start_time = time.time()
        trial = 0
        for t in nx.nonisomorphic_trees(k):
            positive_single_tree(t)
            trial += 1
        print(k, trial, time.time() - start_time)

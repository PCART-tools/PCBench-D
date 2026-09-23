def test_bunch_pickle_generated_with_0_16_and_read_with_0_17():
    bunch = Bunch(key='original')
    # This reproduces a problem when Bunch pickles have been created
    # with scikit-learn 0.16 and are read with 0.17. Basically there
    # is a suprising behaviour because reading bunch.key uses
    # bunch.__dict__ (which is non empty for 0.16 Bunch objects)
    # whereas assigning into bunch.key uses bunch.__setattr__. See
    # https://github.com/scikit-learn/scikit-learn/issues/6196 for
    # more details
    bunch.__dict__['key'] = 'set from __dict__'
    bunch_from_pkl = loads(dumps(bunch))
    # After loading from pickle the __dict__ should have been ignored
    assert_equal(bunch_from_pkl.key, 'original')
    assert_equal(bunch_from_pkl['key'], 'original')
    # Making sure that changing the attr does change the value
    # associated with __getitem__ as well
    bunch_from_pkl.key = 'changed'
    assert_equal(bunch_from_pkl.key, 'changed')
    assert_equal(bunch_from_pkl['key'], 'changed')

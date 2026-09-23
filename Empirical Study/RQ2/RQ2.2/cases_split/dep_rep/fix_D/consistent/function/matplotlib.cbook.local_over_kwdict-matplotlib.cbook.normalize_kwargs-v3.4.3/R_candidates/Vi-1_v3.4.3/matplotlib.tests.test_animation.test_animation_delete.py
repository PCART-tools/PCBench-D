@pytest.mark.parametrize('anim', [dict(klass=dict)], indirect=['anim'])
def test_animation_delete(anim):
    anim = animation.FuncAnimation(**anim)
    with pytest.warns(Warning, match='Animation was deleted'):
        del anim
        gc.collect()

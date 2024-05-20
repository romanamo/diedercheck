from groups import Permutation

def test_apply_permutation():
    p = Permutation([0, 4, 3, 1, 2])
    alphabet = ["a", "b", "c", "d", "e"]

    assert p.apply(alphabet) == ["a", "e", "d", "b", "c"]

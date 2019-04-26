from bokelper import palette, muted_color


def test_palette():
    # default palette
    colors = palette()

    c = next(colors)
    assert c == '#1f77b4'

    # pass palette name
    colors = palette('Category20_3')

    c = next(colors)
    assert c == '#1f77b4'


def test_muted_color():
    # default palette
    colors = palette()
    c = next(colors)
    c = muted_color(c)

    assert c['color']       == '#1f77b4'
    assert c['muted_color'] == '#1f77b4'
    assert c['muted_alpha'] == 0.2

import roots

def test_quadroots_result():
    assert roots.quad_roots(1.0, 1.0, -12.0) == ((3+0j), (-4+0j))

def test_quadroots_types():
    try:
        roots.quad_roots("", "green", "hi")
    except TypeError as err:
        assert(type(err) == TypeError)

def test_quadroots_zerocoeff():
    try:
        roots.quad_roots(a=0.0)
    except ValueError as err:
        assert(type(err) == ValueError)

def test_linearoots_result():
    assert roots.linear_roots(2.0, -3.0) == 1.5

def test_linearroots_types():
    try:
        roots.linear_roots("ocean", 6.0)
    except TypeError as err:
        assert(type(err) == TypeError)

def test_linearroots_zerocoeff():
    try:
        roots.linear_roots(a=0.0)
    except ValueError as err:
        assert(type(err) == ValueError)
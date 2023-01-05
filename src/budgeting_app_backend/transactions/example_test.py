from .example import Example


def test():
    assert isinstance(Example().all(), list)

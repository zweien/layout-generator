import layout_generator.about as about


def test_about():
    assert about.__author__ == "Zweien"
    assert len(about.__version__.split(".")) == 3

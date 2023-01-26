"""Tests to check whether docker is installed, setup and running."""

def test_to_check_if_docker_installed():
    from binocular import Binocular

    response = Binocular()._check_if_docker_is_installed()
    assert isinstance(response, bool)


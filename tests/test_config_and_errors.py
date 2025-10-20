import logging

import pytest

from app.core import config, errors


def test_config_defaults():
    assert config.API_PREFIX == "/api"
    assert config.PROJECT_NAME == "test-py-fastapi"
    assert config.LOGGING_LEVEL in (logging.INFO, logging.DEBUG)


def test_custom_exceptions():
    with pytest.raises(errors.PredictException):
        raise errors.PredictException("test")
    with pytest.raises(errors.ModelLoadException):
        raise errors.ModelLoadException("test")

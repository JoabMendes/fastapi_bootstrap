import json
from unittest.mock import Mock

import pytest
from fastapi import status
from fastapi.exceptions import RequestValidationError
from pydantic import MissingError, ValidationError
from pydantic.error_wrappers import ErrorWrapper

from app.main import validation_exception_handler


@pytest.mark.asyncio
class TestValidationExceptionHandler(object):
    @pytest.fixture
    def missing_field_size(self):
        error_wrapper = ErrorWrapper(
            exc=ValidationError(
                errors=[ErrorWrapper(exc=MissingError(), loc=("size",))],
                model="Model",
            ),
            loc=("body",),
        )
        return error_wrapper

    @pytest.fixture
    def missing_field_name(self):
        error_wrapper = ErrorWrapper(
            exc=ValidationError(
                errors=[ErrorWrapper(exc=MissingError(), loc=("name",))],
                model="Model",
            ),
            loc=("body",),
        )
        return error_wrapper

    @pytest.fixture
    def missing_body(self):
        return ErrorWrapper(
            exc=ValidationError(
                errors=[ErrorWrapper(exc=MissingError(), loc=())],
                model="Model",
            ),
            loc=("body",),
        )

    async def test_should_return_status_code_400(self, missing_field_size):
        request_mock = Mock()

        exception = RequestValidationError([missing_field_size], body=None)
        json_response = await validation_exception_handler(
            request=request_mock, exc=exception
        )

        assert json_response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_should_return_content_with_many_errors(
        self, missing_field_size, missing_field_name
    ):
        request_mock = Mock()

        exception = RequestValidationError(
            [missing_field_size, missing_field_name], body=None
        )
        json_response = await validation_exception_handler(
            request=request_mock, exc=exception
        )

        body_dict = json.loads(json_response.body)
        expected_dict = {
            "detail": [
                {
                    "field": "size",
                    "message": "field required",
                    "type": "value_error.missing",
                },
                {
                    "field": "name",
                    "message": "field required",
                    "type": "value_error.missing",
                },
            ]
        }

        assert body_dict == expected_dict
        assert json_response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_should_return_400_when_request_body_is_empty(
        self, missing_body
    ):
        request_mock = Mock()

        exception = RequestValidationError([missing_body], body=None)
        json_response = await validation_exception_handler(
            request=request_mock, exc=exception
        )

        body_dict = json.loads(json_response.body)
        expected_dict = {
            "detail": [
                {
                    "field": "body",
                    "message": "field required",
                    "type": "value_error.missing",
                }
            ]
        }

        assert body_dict == expected_dict
        assert json_response.status_code == status.HTTP_400_BAD_REQUEST

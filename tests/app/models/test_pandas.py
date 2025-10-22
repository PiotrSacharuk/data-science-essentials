"""
Tests for the Pydantic models in app.models module.
"""

import pytest
from pydantic import ValidationError

from app.models.pandas import DataLoadRequest, DataSliceRequest

BASE_URL = "https://example.com/data.csv"


class TestDataLoadRequest:
    """Test DataLoadRequest Pydantic model."""

    def test_valid_request_required_only(self):
        """Test creating request with only required field."""
        request = DataLoadRequest(source_url=BASE_URL)
        assert request.source_url == BASE_URL
        assert request.separator == ","  # Default value
        assert request.header is True  # Default value

    def test_valid_request_all_fields(self):
        """Test creating request with all fields."""
        request = DataLoadRequest(source_url=BASE_URL, separator=";", header=False)
        assert request.source_url == BASE_URL
        assert request.separator == ";"
        assert request.header is False

    def test_missing_required_field(self):
        """Test that missing required field raises ValidationError."""
        with pytest.raises(ValidationError):
            DataLoadRequest(separator=",", header=True)

    @pytest.mark.parametrize(
        "field,value",
        [
            ("source_url", 123),
            ("separator", 123),
        ],
    )
    def test_invalid_type(self, field, value):
        """Test that invalid types raise ValidationError."""
        with pytest.raises(ValidationError):
            kwargs = {"source_url": BASE_URL, field: value}
            DataLoadRequest(**kwargs)

    def test_header_type_coercion(self):
        """Test type coercion for header field.

        Pydantic coerces compatible types, so string "true" becomes bool True.
        """
        request = DataLoadRequest(source_url=BASE_URL, header="true")
        assert request.header is True

    def test_empty_source_url(self):
        """Test that empty source_url is still valid (let API handle it)."""
        request = DataLoadRequest(source_url="")
        assert request.source_url == ""

    def test_model_json_serialization(self):
        """Test that model can be serialized to JSON."""
        request = DataLoadRequest(
            source_url="https://example.com/data.csv",
            separator=";",
            header=False,
        )
        json_data = request.model_dump()
        assert json_data == {
            "source_url": "https://example.com/data.csv",
            "separator": ";",
            "header": False,
        }

    def test_model_json_deserialization(self):
        """Test that model can be created from JSON."""
        json_data = {
            "source_url": "https://example.com/data.csv",
            "separator": "|",
            "header": True,
        }
        request = DataLoadRequest(**json_data)
        assert request.source_url == "https://example.com/data.csv"
        assert request.separator == "|"
        assert request.header is True


class TestDataSliceRequest:
    """Test DataSliceRequest Pydantic model."""

    def test_valid_request_all_fields(self):
        """Test creating request with all fields."""
        request = DataSliceRequest(
            source_url=BASE_URL,
            separator=";",
            header=False,
            n=10,
        )
        assert request.source_url == BASE_URL
        assert request.separator == ";"
        assert request.header is False
        assert request.n == 10

    def test_valid_request_required_only(self):
        """Test creating request with only required field."""
        request = DataSliceRequest(source_url=BASE_URL)
        assert request.source_url == BASE_URL
        assert request.separator == ","  # Inherited default
        assert request.header is True  # Inherited default
        assert request.n == 5  # Default value

    @pytest.mark.parametrize(
        "n_value",
        [
            0,  # Zero
            -5,  # Negative
            100,  # Custom
            1000000,  # Very large
        ],
    )
    def test_n_values(self, n_value):
        """Test that various n values are accepted by the model."""
        request = DataSliceRequest(source_url=BASE_URL, n=n_value)
        assert request.n == n_value

    def test_invalid_type_n(self):
        """Test type coercion for n field.

        Pydantic coerces compatible types, so string "5" becomes int 5.
        """
        request = DataSliceRequest(source_url=BASE_URL, n="5")
        # Pydantic coerces "5" string to 5 integer
        assert request.n == 5

    def test_missing_required_field(self):
        """Test that missing source_url raises ValidationError."""
        with pytest.raises(ValidationError):
            DataSliceRequest(n=5)

    def test_inheritance_from_dataloadrequest(self):
        """Test that DataSliceRequest inherits from DataLoadRequest."""
        assert issubclass(DataSliceRequest, DataLoadRequest)

    def test_model_json_serialization(self):
        """Test that model can be serialized to JSON."""
        request = DataSliceRequest(
            source_url=BASE_URL, separator=";", header=False, n=20
        )
        json_data = request.model_dump()
        assert json_data == {
            "source_url": BASE_URL,
            "separator": ";",
            "header": False,
            "n": 20,
        }

    def test_model_json_deserialization(self):
        """Test that model can be created from JSON."""
        json_data = {
            "source_url": BASE_URL,
            "separator": "|",
            "header": False,
            "n": 15,
        }
        request = DataSliceRequest(**json_data)
        assert request.source_url == BASE_URL
        assert request.separator == "|"
        assert request.header is False
        assert request.n == 15

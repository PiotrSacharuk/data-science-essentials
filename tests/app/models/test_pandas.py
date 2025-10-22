"""
Tests for the Pydantic models in app.models module.
"""

import pytest
from pydantic import ValidationError

from app.models.pandas import DataLoadRequest, DataSliceRequest


class TestDataLoadRequest:
    """Test DataLoadRequest Pydantic model."""

    def test_valid_request_required_only(self):
        """Test creating request with only required field."""
        request = DataLoadRequest(source_url="https://example.com/data.csv")
        assert request.source_url == "https://example.com/data.csv"
        assert request.separator == ","  # Default value
        assert request.header is True  # Default value

    def test_valid_request_all_fields(self):
        """Test creating request with all fields."""
        request = DataLoadRequest(
            source_url="https://example.com/data.csv",
            separator=";",
            header=False,
        )
        assert request.source_url == "https://example.com/data.csv"
        assert request.separator == ";"
        assert request.header is False

    def test_missing_required_field(self):
        """Test that missing required field raises ValidationError."""
        with pytest.raises(ValidationError):
            DataLoadRequest(separator=",", header=True)

    def test_invalid_type_source_url(self):
        """Test that non-string source_url raises ValidationError."""
        with pytest.raises(ValidationError):
            DataLoadRequest(source_url=123)

    def test_invalid_type_separator(self):
        """Test that non-string separator raises ValidationError."""
        with pytest.raises(ValidationError):
            DataLoadRequest(source_url="https://example.com/data.csv", separator=123)

    def test_invalid_type_header(self):
        """Test type coercion for header field.

        Pydantic coerces compatible types, so string "true" becomes bool True.
        """
        request = DataLoadRequest(
            source_url="https://example.com/data.csv", header="true"
        )
        # Pydantic coerces "true" string to True boolean
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

    def test_valid_request_required_only(self):
        """Test creating request with only required field."""
        request = DataSliceRequest(source_url="https://example.com/data.csv")
        assert request.source_url == "https://example.com/data.csv"
        assert request.separator == ","  # Inherited default
        assert request.header is True  # Inherited default
        assert request.n == 5  # Default value

    def test_valid_request_all_fields(self):
        """Test creating request with all fields."""
        request = DataSliceRequest(
            source_url="https://example.com/data.csv",
            separator=";",
            header=False,
            n=10,
        )
        assert request.source_url == "https://example.com/data.csv"
        assert request.separator == ";"
        assert request.header is False
        assert request.n == 10

    def test_custom_n_value(self):
        """Test creating request with custom n."""
        request = DataSliceRequest(source_url="https://example.com/data.csv", n=100)
        assert request.n == 100

    def test_n_zero(self):
        """Test that n=0 is valid."""
        request = DataSliceRequest(source_url="https://example.com/data.csv", n=0)
        assert request.n == 0

    def test_n_negative(self):
        """Test that negative n is accepted by the model."""
        # Pydantic int validation doesn't restrict negative values by default
        request = DataSliceRequest(source_url="https://example.com/data.csv", n=-5)
        assert request.n == -5

    def test_n_very_large(self):
        """Test that large n values are accepted."""
        request = DataSliceRequest(source_url="https://example.com/data.csv", n=1000000)
        assert request.n == 1000000

    def test_invalid_type_n(self):
        """Test type coercion for n field.

        Pydantic coerces compatible types, so string "5" becomes int 5.
        """
        request = DataSliceRequest(source_url="https://example.com/data.csv", n="5")
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
            source_url="https://example.com/data.csv",
            separator=";",
            header=False,
            n=20,
        )
        json_data = request.model_dump()
        assert json_data == {
            "source_url": "https://example.com/data.csv",
            "separator": ";",
            "header": False,
            "n": 20,
        }

    def test_model_json_deserialization(self):
        """Test that model can be created from JSON."""
        json_data = {
            "source_url": "https://example.com/data.csv",
            "separator": "|",
            "header": False,
            "n": 15,
        }
        request = DataSliceRequest(**json_data)
        assert request.source_url == "https://example.com/data.csv"
        assert request.separator == "|"
        assert request.header is False
        assert request.n == 15

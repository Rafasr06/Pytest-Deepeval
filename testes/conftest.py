import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_banco():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor

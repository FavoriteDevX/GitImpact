import pytest
from unittest.mock import MagicMock, patch
from apps.api.engine.vector_search import SemanticImpactVectorEngine

@pytest.fixture
def mock_vector_engine():
    # Pass a dummy connection string for mocking isolation
    engine = SemanticImpactVectorEngine("postgresql://mock_user:mock_pass@localhost:5432/mock_db")
    return engine

@patch('apps.api.engine.vector_search.OpenAI')
def test_embedding_generation_success(mock_openai_class, mock_vector_engine):
    # Setup deep mock response mimicking OpenAI Vector outputs API structure
    mock_client = MagicMock()
    mock_openai_class.return_url = mock_client
    
    mock_embedding_data = MagicMock()
    mock_embedding_data.embedding = [0.015, -0.023, 0.984, 0.112]
    
    mock_response = MagicMock()
    mock_response.data = [mock_embedding_data]
    
    mock_vector_engine.client.embeddings.create.return_value = mock_response

    # Action execution
    result = mock_vector_engine._generate_embedding("Refactored memory intensive pipeline")

    # Assertions checks
    assert isinstance(result, list)
    assert len(result) == 4
    assert result[2] == 0.984
    mock_vector_engine.client.embeddings.create.assert_called_once_with(
        input=["Refactored memory intensive pipeline"],
        model="text-embedding-3-small"
    )

@patch('apps.api.engine.vector_search.psycopg2.connect')
def test_store_vectorized_highlight_execution(mock_connect, mock_vector_engine):
    # Mocking database cursor behaviors
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Stubs embedding output array internal routing
    mock_vector_engine._generate_embedding = MagicMock(return_value=[0.1, 0.2, 0.3])

    # Execution target
    mock_vector_engine.store_vectorized_highlight("highlight_sha123", "Database indexing optimization context")

    # Validate transactional operations pipeline integrity
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

# Development Guide

## Getting Started

### Prerequisites
- Python 3.9 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Setup Development Environment

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd agentic-ai-bci
   ```

2. **Run the setup script**
   ```bash
   python scripts/setup_dev.py
   ```

3. **Activate virtual environment**
   ```bash
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Initialize data directories**
   ```bash
   python scripts/run_app.py setup
   ```

## Project Structure

```
agentic-ai-bci/
├── src/                     # Source code
│   ├── agents/             # LangChain agents
│   │   ├── __init__.py
│   │   ├── base_agent.py   # Base agent class
│   │   ├── data_query_agent.py
│   │   ├── analysis_agent.py
│   │   ├── planning_agent.py
│   │   └── coordinator_agent.py
│   ├── models/             # Data models
│   │   ├── __init__.py
│   │   ├── dataset.py      # Dataset models
│   │   ├── experiment.py   # Experiment models
│   │   ├── analysis.py     # Analysis models
│   │   └── user.py         # User models
│   ├── services/           # Business logic
│   │   ├── __init__.py
│   │   ├── dataset_service.py
│   │   ├── analysis_service.py
│   │   ├── literature_service.py
│   │   └── experiment_service.py
│   ├── api/                # FastAPI routes
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI app
│   │   ├── routes/         # API routes
│   │   └── middleware/     # Custom middleware
│   ├── ui/                 # User interface
│   │   ├── __init__.py
│   │   ├── streamlit_app.py
│   │   └── components/     # UI components
│   └── utils/              # Utility functions
│       ├── __init__.py
│       ├── logging.py
│       ├── validation.py
│       └── helpers.py
├── tests/                  # Test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── fixtures/           # Test data
├── scripts/                # Utility scripts
├── docs/                   # Documentation
├── data/                   # Data storage
└── config/                 # Configuration files
```

## Development Workflow

### 1. Creating New Features

1. **Create a feature branch**
   ```bash
   git checkout -b feature/new-agent-functionality
   ```

2. **Write tests first (TDD)**
   ```bash
   # Create test file
   touch tests/unit/test_new_feature.py
   ```

3. **Implement the feature**
   ```python
   # Follow the existing patterns
   # Use type hints
   # Add docstrings
   ```

4. **Run tests**
   ```bash
   pytest tests/
   ```

5. **Format code**
   ```bash
   black src tests
   flake8 src tests
   mypy src
   ```

### 2. Agent Development

#### Base Agent Pattern
```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from langchain.agents import AgentExecutor
from langchain.schema import BaseMessage

class BaseAgent(ABC):
    """Base class for all agents."""
    
    def __init__(self, llm, tools: List[Any]):
        self.llm = llm
        self.tools = tools
        self.executor = self._create_executor()
    
    @abstractmethod
    def _create_executor(self) -> AgentExecutor:
        """Create the agent executor."""
        pass
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent with input data."""
        result = await self.executor.arun(input_data)
        return self._format_output(result)
    
    @abstractmethod
    def _format_output(self, result: Any) -> Dict[str, Any]:
        """Format the agent output."""
        pass
```

#### Creating a New Agent
1. Inherit from `BaseAgent`
2. Define specific tools needed
3. Implement the executor creation
4. Add to the agent registry

### 3. Service Development

#### Service Pattern
```python
from typing import List, Optional
from sqlalchemy.orm import Session
from src.models import Dataset

class DatasetService:
    """Service for dataset operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def list_datasets(
        self, 
        source: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> List[Dataset]:
        """List datasets with filtering."""
        query = self.db.query(Dataset)
        
        if source:
            query = query.filter(Dataset.source == source)
        
        return query.offset(offset).limit(limit).all()
    
    async def get_dataset(self, dataset_id: str) -> Optional[Dataset]:
        """Get a specific dataset."""
        return self.db.query(Dataset).filter(
            Dataset.id == dataset_id
        ).first()
```

### 4. API Development

#### Route Structure
```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.services.dataset_service import DatasetService
from src.models.dataset import DatasetResponse

router = APIRouter(prefix="/datasets", tags=["datasets"])

@router.get("/", response_model=List[DatasetResponse])
async def list_datasets(
    source: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    service: DatasetService = Depends(get_dataset_service)
):
    """List available datasets."""
    datasets = await service.list_datasets(source, limit, offset)
    return [DatasetResponse.from_orm(ds) for ds in datasets]
```

### 5. Testing Guidelines

#### Unit Testing
```python
import pytest
from unittest.mock import Mock, AsyncMock
from src.agents.data_query_agent import DataQueryAgent

@pytest.fixture
def mock_llm():
    return Mock()

@pytest.fixture
def mock_tools():
    return [Mock(), Mock()]

@pytest.mark.asyncio
async def test_data_query_agent_run(mock_llm, mock_tools):
    """Test data query agent execution."""
    agent = DataQueryAgent(mock_llm, mock_tools)
    
    input_data = {"query": "Find EEG datasets"}
    result = await agent.run(input_data)
    
    assert "datasets" in result
    assert isinstance(result["datasets"], list)
```

#### Integration Testing
```python
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_list_datasets_endpoint():
    """Test the datasets listing endpoint."""
    response = client.get("/api/v1/datasets")
    
    assert response.status_code == 200
    data = response.json()
    assert "datasets" in data
```

### 6. Configuration Management

#### Environment Variables
Use the `Settings` class for configuration:

```python
from src.config import settings

# Access configuration
api_key = settings.anthropic_api_key
database_url = settings.database_url
```

#### Adding New Configuration
1. Add field to `Settings` class
2. Update `.env.example`
3. Document in configuration guide

## Code Style Guidelines

### Python Style
- Follow PEP 8
- Use Black for formatting
- Maximum line length: 88 characters
- Use type hints for all functions
- Write docstrings for all public methods

### Naming Conventions
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`

### Import Organization
```python
# Standard library imports
import os
import sys
from typing import List, Optional

# Third-party imports
import numpy as np
import pandas as pd
from fastapi import FastAPI
from langchain.agents import Agent

# Local imports
from src.config import settings
from src.models.dataset import Dataset
```

## Database Development

### Models
Use SQLAlchemy ORM for database models:

```python
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Dataset(Base):
    __tablename__ = "datasets"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    source = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### Migrations
Use Alembic for database migrations:

```bash
# Create migration
alembic revision --autogenerate -m "Add dataset table"

# Apply migration
alembic upgrade head
```

## Performance Guidelines

### Async Operations
Use async/await for I/O operations:

```python
async def fetch_dataset(dataset_id: str) -> Dataset:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/datasets/{dataset_id}")
        return Dataset.parse_obj(response.json())
```

### Caching
Implement caching for expensive operations:

```python
from functools import lru_cache
import asyncio

@lru_cache(maxsize=128)
def expensive_computation(data: str) -> str:
    # Expensive operation
    return result
```

### Database Optimization
- Use database indexes appropriately
- Implement pagination for large datasets
- Use connection pooling

## Security Considerations

### API Security
- Validate all inputs
- Use authentication for sensitive endpoints
- Implement rate limiting
- Sanitize user inputs

### Data Protection
- Never log sensitive data
- Encrypt data at rest and in transit
- Follow GDPR guidelines for user data

## Debugging and Logging

### Logging Setup
```python
import logging
from src.utils.logging import setup_logging

# Configure logging
setup_logging(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use structured logging
logger.info("Processing dataset", extra={
    "dataset_id": dataset_id,
    "user_id": user_id
})
```

### Debugging Tools
- Use `breakpoint()` for debugging
- pytest with `-v` for verbose output
- Use logging instead of print statements

## Documentation

### Code Documentation
- Write clear docstrings
- Use type hints
- Include examples in docstrings

```python
def analyze_signal_quality(
    signal_data: np.ndarray,
    sampling_rate: int,
    frequency_bands: Dict[str, Tuple[float, float]]
) -> Dict[str, float]:
    """Analyze the quality of neural signal data.
    
    Args:
        signal_data: EEG/MEG signal data with shape (channels, samples)
        sampling_rate: Sampling rate in Hz
        frequency_bands: Dictionary mapping band names to (low, high) frequencies
        
    Returns:
        Dictionary containing quality metrics for each frequency band
        
    Example:
        >>> signal = np.random.randn(64, 1000)
        >>> bands = {"alpha": (8, 12), "beta": (13, 30)}
        >>> quality = analyze_signal_quality(signal, 256, bands)
        >>> quality["alpha"]
        0.85
    """
```

### API Documentation
- Use FastAPI automatic documentation
- Add detailed descriptions to endpoints
- Include request/response examples

## Deployment

### Docker
Build and run with Docker:

```bash
# Build image
docker build -t agentic-ai-bci .

# Run container
docker run -p 8000:8000 -p 8501:8501 agentic-ai-bci
```

### Environment Setup
- Use environment-specific configuration
- Set up CI/CD pipeline
- Configure monitoring and logging

## Contributing

### Pull Request Process
1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Ensure all tests pass
5. Submit pull request with clear description

### Code Review Guidelines
- Review for functionality and style
- Check test coverage
- Verify documentation updates
- Test locally before approval

## Troubleshooting

### Common Issues
1. **Import errors**: Check Python path and virtual environment
2. **API key errors**: Verify environment variables
3. **Database connection**: Check database URL and permissions
4. **Port conflicts**: Ensure ports 8000 and 8501 are available

### Getting Help
- Check existing issues in GitHub
- Review documentation
- Ask in team chat or meetings
- Create detailed bug reports with reproduction steps

# API Documentation

## Overview

The Agentic AI BCI Research Assistant provides a RESTful API for interacting with the system programmatically. The API is built using FastAPI and provides endpoints for dataset management, analysis execution, and research assistance.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

The API uses JWT tokens for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Health Check

#### GET /health
Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-09T12:00:00Z",
  "version": "1.0.0"
}
```

### Datasets

#### GET /datasets
List available datasets.

**Parameters:**
- `source` (optional): Filter by data source (openneuro, physionet)
- `limit` (optional): Maximum number of results (default: 10)
- `offset` (optional): Number of results to skip (default: 0)

**Response:**
```json
{
  "datasets": [
    {
      "id": "ds001",
      "name": "Motor Imagery EEG Dataset",
      "description": "64-channel EEG data for motor imagery tasks",
      "source": "openneuro",
      "subjects": 10,
      "tasks": ["motor_imagery", "rest"],
      "metadata": {
        "sampling_rate": 256,
        "channels": 64,
        "sessions": 2
      }
    }
  ],
  "total": 1,
  "limit": 10,
  "offset": 0
}
```

#### GET /datasets/{dataset_id}
Get detailed information about a specific dataset.

**Response:**
```json
{
  "id": "ds001",
  "name": "Motor Imagery EEG Dataset",
  "description": "Detailed description...",
  "source": "openneuro",
  "metadata": {
    "subjects": 10,
    "tasks": ["motor_imagery", "rest"],
    "sampling_rate": 256,
    "channels": 64,
    "sessions": 2,
    "file_format": "BDF",
    "created": "2024-01-01",
    "ethics_approval": "IRB-2024-001"
  },
  "files": [
    {
      "subject": "sub-01",
      "session": "ses-01",
      "task": "motor_imagery",
      "file_path": "sub-01/ses-01/eeg/sub-01_ses-01_task-motor_eeg.bdf",
      "size_mb": 45.2
    }
  ]
}
```

#### POST /datasets/search
Search datasets using natural language queries.

**Request Body:**
```json
{
  "query": "Find EEG datasets with motor imagery tasks and at least 50 subjects",
  "filters": {
    "modality": ["EEG"],
    "min_subjects": 50,
    "tasks": ["motor_imagery"]
  }
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "ds001",
      "name": "Large-scale Motor Imagery Study",
      "relevance_score": 0.95,
      "match_reasons": [
        "Contains motor imagery tasks",
        "Has 100 subjects (exceeds minimum)",
        "Uses EEG modality"
      ]
    }
  ],
  "query_interpretation": "Looking for EEG datasets focused on motor imagery with large sample sizes"
}
```

### Analysis

#### POST /analysis/signal-quality
Assess the quality of neural signals.

**Request Body:**
```json
{
  "dataset_id": "ds001",
  "subject_id": "sub-01",
  "session_id": "ses-01",
  "analysis_params": {
    "frequency_bands": {
      "alpha": [8, 12],
      "beta": [13, 30]
    },
    "artifact_detection": true,
    "channel_quality": true
  }
}
```

**Response:**
```json
{
  "analysis_id": "analysis-123",
  "status": "completed",
  "results": {
    "overall_quality": "good",
    "quality_score": 0.85,
    "channel_quality": {
      "good_channels": 58,
      "poor_channels": 6,
      "bad_channels": ["Ch32", "Ch45"]
    },
    "artifacts": {
      "eye_blinks": 45,
      "muscle_artifacts": 12,
      "line_noise": "minimal"
    },
    "spectral_analysis": {
      "alpha_power": 12.5,
      "beta_power": 8.3,
      "peak_alpha_frequency": 10.2
    }
  },
  "recommendations": [
    "Consider excluding channels Ch32 and Ch45",
    "Apply notch filter at 50Hz for line noise",
    "Use ICA for eye blink removal"
  ]
}
```

#### POST /analysis/experiment-plan
Generate an experiment plan using AI assistance.

**Request Body:**
```json
{
  "research_question": "How does motor imagery training affect alpha rhythm modulation in stroke patients?",
  "constraints": {
    "budget": "low",
    "duration_weeks": 8,
    "participant_pool": "stroke_patients",
    "equipment": ["EEG_64ch", "computer"]
  },
  "preferences": {
    "paradigm": "motor_imagery",
    "analysis_methods": ["spectral_analysis", "connectivity"]
  }
}
```

**Response:**
```json
{
  "plan_id": "plan-456",
  "experiment_design": {
    "title": "Alpha Rhythm Modulation in Stroke Rehabilitation",
    "objective": "Investigate alpha rhythm changes during motor imagery training",
    "participants": {
      "target_n": 20,
      "inclusion_criteria": [
        "Stroke patients 6+ months post-stroke",
        "Mild to moderate motor impairment",
        "Age 18-75"
      ],
      "exclusion_criteria": [
        "Severe cognitive impairment",
        "Epilepsy history",
        "Metallic implants"
      ]
    },
    "protocol": {
      "sessions": 16,
      "duration_per_session": "45 minutes",
      "tasks": [
        {
          "name": "baseline_recording",
          "duration": "5 minutes",
          "description": "Resting state EEG"
        },
        {
          "name": "motor_imagery",
          "duration": "30 minutes",
          "trials": 100,
          "description": "Imagined hand movements"
        }
      ]
    },
    "analysis_plan": [
      "Spectral power analysis in alpha band (8-12 Hz)",
      "Event-related desynchronization (ERD) analysis",
      "Functional connectivity changes",
      "Clinical correlation analysis"
    ]
  },
  "estimated_timeline": {
    "recruitment": "2 weeks",
    "data_collection": "8 weeks",
    "analysis": "4 weeks",
    "total": "14 weeks"
  },
  "budget_estimate": {
    "personnel": "$5000",
    "equipment": "$0 (existing)",
    "participant_compensation": "$2000",
    "total": "$7000"
  }
}
```

### Literature

#### POST /literature/search
Search relevant literature using AI-powered semantic search.

**Request Body:**
```json
{
  "query": "motor imagery BCI stroke rehabilitation alpha rhythm",
  "filters": {
    "publication_years": [2020, 2025],
    "study_types": ["randomized_controlled_trial", "clinical_study"],
    "max_results": 20
  }
}
```

**Response:**
```json
{
  "papers": [
    {
      "title": "Alpha Rhythm Enhancement in Stroke Patients Through Motor Imagery Training",
      "authors": ["Smith, J.", "Johnson, A."],
      "journal": "Journal of Neural Engineering",
      "year": 2023,
      "doi": "10.1088/1741-2552/abc123",
      "relevance_score": 0.92,
      "abstract": "This study investigated...",
      "key_findings": [
        "Significant alpha power increase after training",
        "Improved motor function correlation with alpha changes"
      ],
      "methodology": {
        "participants": 25,
        "duration": "6 weeks",
        "equipment": "64-channel EEG"
      }
    }
  ],
  "summary": {
    "total_papers": 15,
    "key_themes": ["alpha rhythm modulation", "motor imagery training", "stroke rehabilitation"],
    "research_gaps": [
      "Limited long-term follow-up studies",
      "Need for larger sample sizes"
    ]
  }
}
```

#### POST /literature/summarize
Generate a literature review summary.

**Request Body:**
```json
{
  "topic": "motor imagery BCI for stroke rehabilitation",
  "paper_ids": ["paper1", "paper2", "paper3"],
  "focus_areas": ["methodology", "outcomes", "limitations"]
}
```

### Chat

#### POST /chat
Interact with the AI research assistant.

**Request Body:**
```json
{
  "message": "What's the best EEG frequency band for motor imagery classification?",
  "context": {
    "current_project": "stroke_rehabilitation_study",
    "previous_messages": ["Hello", "I'm working on a motor imagery study"]
  }
}
```

**Response:**
```json
{
  "response": "For motor imagery classification, the most informative frequency bands are typically:\n\n1. **Mu rhythm (8-12 Hz)**: Shows strong desynchronization during motor imagery\n2. **Beta band (13-30 Hz)**: Particularly the sensorimotor beta rhythm\n3. **Gamma band (30-100 Hz)**: Can provide additional discriminative information\n\nFor stroke patients specifically, you might want to focus on the mu rhythm as it's often preserved and shows clear modulation during motor imagery tasks.",
  "citations": [
    {
      "title": "Motor imagery classification using mu and beta rhythms",
      "authors": ["Pfurtscheller, G."],
      "year": 2020
    }
  ],
  "suggestions": [
    "Consider individual alpha frequency (IAF) adjustment",
    "Use adaptive frequency band selection",
    "Analyze both hemispheres for stroke patients"
  ]
}
```

## Error Handling

All endpoints return appropriate HTTP status codes and error messages:

### Error Response Format
```json
{
  "error": {
    "code": "DATASET_NOT_FOUND",
    "message": "Dataset with ID 'invalid_id' not found",
    "details": {
      "available_datasets": ["ds001", "ds002", "ds003"]
    }
  },
  "timestamp": "2025-01-09T12:00:00Z",
  "request_id": "req-789"
}
```

### Common Error Codes
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## Rate Limiting

The API implements rate limiting to ensure fair usage:
- 100 requests per minute per API key
- 1000 requests per hour per API key
- Analysis endpoints: 10 requests per minute

## SDK and Examples

### Python SDK
```python
from bci_assistant import BCIAssistantClient

client = BCIAssistantClient(api_key="your_api_key")

# Search datasets
datasets = client.datasets.search("motor imagery EEG")

# Analyze signal quality
analysis = client.analysis.signal_quality(
    dataset_id="ds001",
    subject_id="sub-01"
)

# Chat with AI assistant
response = client.chat.send("What's the best preprocessing pipeline for EEG?")
```

### cURL Examples
```bash
# Get datasets
curl -H "Authorization: Bearer $API_KEY" \
     http://localhost:8000/api/v1/datasets

# Search literature
curl -X POST \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"query": "motor imagery stroke rehabilitation"}' \
     http://localhost:8000/api/v1/literature/search
```

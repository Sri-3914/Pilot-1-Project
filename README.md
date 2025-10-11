# Stravito Query Orchestrator

A FastAPI backend with Streamlit UI that processes queries through multiple analytical angles using the Stravito API and synthesizes comprehensive reports using Azure OpenAI.

## Features

- **Multi-Angle Analysis**: Automatically generates multiple analytical perspectives for each query
- **Parallel Processing**: Uses asyncio to process all angles simultaneously for faster results
- **Contradiction Detection**: Identifies and analyzes contradictions between different angle responses
- **Intelligent Synthesis**: Uses Azure OpenAI to create comprehensive, structured reports
- **Citation System**: ChatGPT-style source attribution with clickable citations and references
- **Modern UI**: Clean Streamlit interface with real-time progress tracking
- **Robust Error Handling**: Graceful handling of API failures and edge cases

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │───▶│   FastAPI       │───▶│   Stravito API  │
│   (Frontend)    │    │   (Backend)     │    │   (Data Source) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Azure OpenAI  │
                       │   (Synthesis)   │
                       └─────────────────┘
```

## Prerequisites

- Python 3.8+
- Stravito API access with API key
- Azure OpenAI service with API key and deployment

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Pilot-1-Project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` file with your actual credentials:
   ```env
   # Stravito API Configuration
   IHUB_API_KEY=your_actual_stravito_api_key
   IHUB_BASE_URL=https://your-actual-stravito-base-url.com

   # Azure OpenAI Configuration
   AZURE_OPENAI_API_KEY=your_actual_azure_openai_api_key
   AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   AZURE_OPENAI_DEPLOYMENT_NAME=your-actual-deployment-name
   ```

## Usage

### 1. Start the FastAPI Backend

```bash
# Option 1: Direct Python execution
python main.py

# Option 2: Using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### 2. Start the Streamlit Frontend

In a new terminal:

```bash
streamlit run streamlit_app.py
```

The UI will be available at `http://localhost:8501`

### 3. Using the Application

1. Open your browser and go to `http://localhost:8501`
2. Enter your query in the text area
3. Click "Process Query" to start the analysis
4. Wait for the multi-angle processing to complete
5. Review the synthesized report and detailed analysis
6. Click on citation badges to view source documents
7. Explore individual sources in the dedicated Sources section

#### Citations and Sources

The application now includes a comprehensive citation system:

- **Quick Citation Badges**: Clickable numbered badges ([1], [2], etc.) at the end of the report
- **Source Cards**: Detailed cards showing title, excerpt, page number, and clickable links
- **Per-Angle Sources**: See which sources contributed to each analytical angle
- **Interactive Links**: Click any source to open the original document in a new tab

For detailed information about the citation system, see [CITATIONS_GUIDE.md](CITATIONS_GUIDE.md).

## API Endpoints

### FastAPI Backend (`http://localhost:8000`)

- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /query` - Process a query through orchestration
- `GET /docs` - Interactive API documentation (Swagger UI)

### Example API Usage

```python
import requests

# Process a query
response = requests.post(
    "http://localhost:8000/query",
    json={"query": "What are the latest trends in AI?"}
)

result = response.json()
print(result["final_report"]["synthesized_report"])
```

## Project Structure

```
Pilot-1-Project/
├── main.py                 # FastAPI application
├── orchestrator.py         # Core orchestration logic
├── stravito_client.py      # Stravito API client
├── config.py              # Configuration management
├── streamlit_app.py       # Streamlit UI with citation display
├── requirements.txt       # Python dependencies
├── env.example           # Environment variables template
├── README.md             # This file
└── CITATIONS_GUIDE.md    # Detailed citation system documentation
```

## How It Works

1. **Query Input**: User submits a query through the Streamlit UI
2. **Angle Generation**: Azure OpenAI generates multiple analytical angles
3. **Parallel Processing**: Each angle is processed through Stravito API simultaneously
4. **Response Normalization**: Raw responses are cleaned and structured, sources are extracted
5. **Contradiction Analysis**: AI analyzes responses for conflicts or inconsistencies
6. **Source Collection**: Citations are collected and deduplicated across all angles
7. **Report Synthesis**: Azure OpenAI creates a comprehensive, structured report
8. **Results Display**: Streamlit UI presents the final report with interactive citations and source cards

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `IHUB_API_KEY` | Stravito API key | Yes |
| `IHUB_BASE_URL` | Stravito API base URL | Yes |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | Yes |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | Yes |
| `AZURE_OPENAI_API_VERSION` | Azure OpenAI API version | No (default: 2024-02-15-preview) |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Azure OpenAI deployment name | Yes |

### Customization

- **API Timeout**: Modify timeout values in `streamlit_app.py` and `orchestrator.py`
- **Angle Count**: Adjust the number of analytical angles in `orchestrator.py`
- **UI Theme**: Customize Streamlit appearance in `streamlit_app.py`

## Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Verify environment variables are set correctly
   - Check if FastAPI server is running on port 8000
   - Ensure Stravito API credentials are valid

2. **Azure OpenAI Errors**
   - Verify Azure OpenAI deployment is active
   - Check API key and endpoint URL
   - Ensure deployment name matches your configuration

3. **Timeout Errors**
   - Increase timeout values for complex queries
   - Check network connectivity
   - Verify Stravito API response times

### Logs

- FastAPI logs: Check terminal where `main.py` is running
- Streamlit logs: Check terminal where `streamlit_app.py` is running

## Development

### Adding New Features

1. **New API Endpoints**: Add to `main.py`
2. **Orchestration Logic**: Modify `orchestrator.py`
3. **UI Components**: Update `streamlit_app.py`
4. **API Client**: Extend `stravito_client.py`

### Testing

```bash
# Test FastAPI endpoints
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "test query"}'

# Test health endpoint
curl http://localhost:8000/health
```

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation at `http://localhost:8000/docs`
3. Check environment variable configuration
4. Verify all services are running correctly

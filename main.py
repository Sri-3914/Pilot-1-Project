from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import asyncio
from orchestrator import QueryOrchestrator

app = FastAPI(
    title="XXXX Query Orchestrator",
    description="FastAPI backend for orchestrating multi-angle queries through XXXX API with Azure OpenAI synthesis",
    version="1.0.0"
)

# Add CORS middleware for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Streamlit domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = QueryOrchestrator()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    success: bool
    original_query: str
    angles_generated: list = []
    responses_processed: int = 0
    final_report: Dict[str, Any] = {}
    raw_responses: list = []
    error: str = None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "XXXX Query Orchestrator API is running"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "XXXX Query Orchestrator",
        "version": "1.0.0"
    }

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a query through multi-angle analysis and synthesis
    
    This endpoint:
    1. Generates multiple analytical angles for the query
    2. Processes each angle through XXXX API in parallel
    3. Normalizes and analyzes responses for contradictions
    4. Synthesizes a comprehensive report using Azure OpenAI
    """
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Process the query through orchestration
        result = await orchestrator.orchestrate_query(request.query)
        
        return QueryResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/query/{query_id}")
async def get_query_status(query_id: str):
    """
    Get the status of a previously submitted query
    Note: This is a placeholder for future implementation of async query processing
    """
    return {"message": f"Query status for {query_id} not implemented yet"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

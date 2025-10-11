from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import asyncio
import sys

# Initialize FastAPI app first
app = FastAPI(
    title="Stravito Query Orchestrator",
    description="FastAPI backend for orchestrating multi-angle queries through Stravito API with Azure OpenAI synthesis",
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

# Initialize orchestrator with error handling
orchestrator = None

@app.on_event("startup")
async def startup_event():
    """Initialize orchestrator on startup with proper error handling"""
    global orchestrator
    try:
        print("🚀 Starting Stravito Query Orchestrator...")
        print("📋 Checking configuration...")
        
        # Import here to catch configuration errors
        from orchestrator import QueryOrchestrator
        
        print("✅ Configuration validated")
        print("🔧 Initializing orchestrator...")
        
        orchestrator = QueryOrchestrator()
        
        print("✅ Orchestrator initialized successfully")
        print("🌐 Server is ready to accept requests")
        
    except ValueError as e:
        print("\n" + "="*80)
        print("❌ CONFIGURATION ERROR")
        print("="*80)
        print(f"\n{e}\n")
        print("Please check your .env file and ensure all required variables are set.")
        print("Run 'python diagnose_startup.py' for detailed diagnostics.\n")
        print("="*80 + "\n")
        sys.exit(1)
    except Exception as e:
        print("\n" + "="*80)
        print("❌ STARTUP ERROR")
        print("="*80)
        print(f"\nError: {e}\n")
        print("Run 'python diagnose_startup.py' for detailed diagnostics.\n")
        print("="*80 + "\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)

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
    return {"message": "Stravito Query Orchestrator API is running"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "Stravito Query Orchestrator",
        "version": "1.0.0"
    }

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a query through multi-angle analysis and synthesis
    
    This endpoint:
    1. Generates multiple analytical angles for the query
    2. Processes each angle through Stravito API in parallel
    3. Normalizes and analyzes responses for contradictions
    4. Synthesizes a comprehensive report using Azure OpenAI
    """
    try:
        if orchestrator is None:
            raise HTTPException(
                status_code=503, 
                detail="Service not ready. Orchestrator failed to initialize. Check server logs."
            )
        
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        print(f"\n[MAIN] ========== NEW QUERY REQUEST ==========")
        print(f"[MAIN] Query: {request.query[:100]}...")
        
        # Process the query through orchestration
        result = await orchestrator.orchestrate_query(request.query)
        
        # Log source information being returned to frontend
        final_report = result.get("final_report", {})
        sources = final_report.get("sources", [])
        
        print(f"\n[MAIN] ========== SENDING RESPONSE TO FRONTEND ==========")
        print(f"[MAIN] Success: {result.get('success', False)}")
        print(f"[MAIN] Sources in final_report: {len(sources)}")
        
        if sources:
            print(f"[MAIN] Source details being sent:")
            for i, source in enumerate(sources):
                print(f"[MAIN]   [{i+1}] {source.get('title', 'Untitled')[:50]}")
                print(f"[MAIN]       URL: {source.get('url', 'N/A')}")
                print(f"[MAIN]       Page: {source.get('pageNumber', 'N/A')}")
        else:
            print(f"[MAIN] ⚠️  WARNING: No sources being sent to frontend!")
        
        # Also log raw_responses sources
        raw_responses = result.get("raw_responses", [])
        total_raw_sources = sum(len(r.get('sources', [])) for r in raw_responses)
        print(f"[MAIN] Total sources in raw_responses: {total_raw_sources}")
        
        print(f"[MAIN] ========================================\n")
        
        return QueryResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[MAIN] ❌ Error processing query: {e}")
        import traceback
        traceback.print_exc()
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

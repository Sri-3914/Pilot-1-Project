import streamlit as st
import requests
import json
import time
from typing import Dict, Any

# Configure Streamlit page
st.set_page_config(
    page_title="Stravito Query Orchestrator",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

def call_api(query: str) -> Dict[str, Any]:
    """Call the FastAPI backend to process a query"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            json={"query": query},
            timeout=300  # 5 minute timeout for complex queries
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

def display_loading_animation():
    """Display a loading animation while processing"""
    with st.spinner("Processing your query through multiple analytical angles..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simulate progress steps
        steps = [
            "Generating analytical angles...",
            "Processing through Stravito API...",
            "Normalizing responses...",
            "Checking for contradictions...",
            "Synthesizing final report..."
        ]
        
        for i, step in enumerate(steps):
            status_text.text(step)
            progress_bar.progress((i + 1) / len(steps))
            time.sleep(0.5)
        
        status_text.text("Finalizing results...")
        progress_bar.progress(1.0)

def display_query_result(result: Dict[str, Any]):
    """Display the query processing results"""
    if not result:
        return
    
    if not result.get("success", False):
        st.error(f"Query processing failed: {result.get('error', 'Unknown error')}")
        return
    
    # Main results section
    st.success("✅ Query processed successfully!")
    
    # Original query
    st.subheader("📝 Original Query")
    st.info(result.get("original_query", ""))
    
    # Final synthesized report
    st.subheader("📊 Synthesized Report")
    final_report = result.get("final_report", {})
    
    if final_report.get("error"):
        st.error(f"Report synthesis failed: {final_report['error']}")
    else:
        # Display the synthesized report in an expandable section
        with st.expander("View Complete Report", expanded=True):
            st.markdown(final_report.get("synthesized_report", "No report generated"))
    
    # Processing statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Angles Generated", result.get("responses_processed", 0))
    with col2:
        st.metric("Responses Processed", result.get("responses_processed", 0))
    with col3:
        st.metric("Processing Time", f"{final_report.get('timestamp', 0):.2f}s")
    
    # Detailed analysis sections
    st.subheader("🔍 Detailed Analysis")
    
    # Analytical angles
    angles = result.get("angles_generated", [])
    if angles:
        st.write("**Analytical Angles Generated:**")
        for i, angle in enumerate(angles, 1):
            st.write(f"{i}. {angle}")
    
    # Raw responses (collapsible)
    raw_responses = result.get("raw_responses", [])
    if raw_responses:
        with st.expander("View Raw Responses from Each Angle"):
            for i, response in enumerate(raw_responses):
                st.write(f"**Angle {i+1}: {response.get('angle', 'Unknown')}**")
                st.write(f"*Status: {response.get('status', 'Unknown')}*")
                
                content = response.get('content', '')
                if content:
                    st.write(content[:500] + "..." if len(content) > 500 else content)
                else:
                    st.write("*No content available*")
                
                # Contradiction analysis if available
                if response.get('contradiction_analysis'):
                    st.write("**Contradiction Analysis:**")
                    st.write(response['contradiction_analysis'])
                
                st.divider()

def main():
    """Main Streamlit application"""
    
    # Header
    st.title("🔍 Stravito Query Orchestrator")
    st.markdown("""
    This application processes your queries through multiple analytical angles using the Stravito API, 
    then synthesizes comprehensive reports using Azure OpenAI.
    """)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Status check
        try:
            health_response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if health_response.status_code == 200:
                st.success("✅ API Connected")
            else:
                st.error("❌ API Connection Failed")
        except:
            st.error("❌ API Unavailable")
            st.info("Make sure the FastAPI server is running on port 8000")
        
        st.divider()
        
        # Instructions
        st.header("📖 How to Use")
        st.markdown("""
        1. Enter your query in the text area
        2. Click 'Process Query' to start analysis
        3. Wait for multi-angle processing
        4. Review the synthesized report
        5. Explore detailed responses
        """)
        
        st.divider()
        
        # Example queries
        st.header("💡 Example Queries")
        example_queries = [
            "What are the latest trends in artificial intelligence?",
            "How is climate change affecting global markets?",
            "What are the key challenges in renewable energy adoption?",
            "Analyze the impact of remote work on productivity"
        ]
        
        st.markdown("**Try these example queries:**")
        for i, query in enumerate(example_queries, 1):
            st.markdown(f"{i}. {query}")
    
    # Main content area
    st.header("🎯 Query Input")
    
    # Query input
    query = st.text_area(
        "Enter your query:",
        height=100,
        placeholder="Type your question here... The system will analyze it from multiple angles and provide a comprehensive report."
    )
    
    # Process button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        process_button = st.button("🚀 Process Query", type="primary", use_container_width=True)
    
    # Process the query
    if process_button and query.strip():
        # Display loading animation
        display_loading_animation()
        
        # Call API
        result = call_api(query.strip())
        
        # Display results
        if result:
            display_query_result(result)
    
    elif process_button and not query.strip():
        st.warning("⚠️ Please enter a query before processing.")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Stravito Query Orchestrator | Powered by FastAPI, Streamlit, and Azure OpenAI</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

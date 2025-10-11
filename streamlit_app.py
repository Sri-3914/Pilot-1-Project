import streamlit as st
import requests
import json
import time
from typing import Dict, Any, List

# Configure Streamlit page
st.set_page_config(
    page_title="Stravito Query Orchestrator",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better citation styling
st.markdown("""
<style>
    /* Citation card styling */
    .citation-card {
        background-color: #f8f9fa;
        border-left: 4px solid #4CAF50;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .citation-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .citation-number {
        display: inline-block;
        background-color: #4CAF50;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        margin-right: 10px;
        font-size: 0.9em;
    }
    
    .citation-title {
        color: #1976D2;
        font-weight: 600;
        font-size: 1.1em;
        margin: 8px 0;
    }
    
    .citation-excerpt {
        color: #555;
        font-style: italic;
        margin: 8px 0;
        line-height: 1.5;
    }
    
    .citation-meta {
        color: #888;
        font-size: 0.85em;
        margin-top: 8px;
    }
    
    /* Source badge styling */
    .source-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.75em;
        font-weight: bold;
        margin: 0 4px;
        text-decoration: none;
    }
    
    .source-badge:hover {
        opacity: 0.8;
    }
</style>
""", unsafe_allow_html=True)

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

def add_citation_links(text: str, sources: List[Dict[str, Any]]) -> str:
    """Add inline citation links to the text"""
    if not sources or not text:
        return text
    
    # Add citation summary at the end of text
    citation_html = "<br><br><div style='margin-top: 20px; padding-top: 20px; border-top: 2px solid #eee;'>"
    citation_html += "<strong>📎 Quick Citations:</strong><br>"
    
    for i, source in enumerate(sources):
        title = source.get('title', 'Source')[:50]  # Truncate long titles
        url = source.get('url', '')
        if url:
            citation_html += f'<a href="{url}" target="_blank" class="source-badge">[{i+1}]</a> '
        else:
            citation_html += f'<span class="source-badge">[{i+1}]</span> '
    
    citation_html += "</div>"
    
    return text + citation_html

def display_sources(sources: List[Dict[str, Any]]):
    """Display sources as clickable citations similar to ChatGPT"""
    if not sources:
        return
    
    st.subheader("📚 Sources")
    st.markdown("*Click on any source to view the original document*")
    
    # Display sources in a grid layout
    cols_per_row = 2
    for i in range(0, len(sources), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(sources):
                source = sources[idx]
                with col:
                    # Create a styled citation card
                    title = source.get('title', 'Untitled Document')
                    url = source.get('url', '')
                    text = source.get('text', '')
                    page_number = source.get('pageNumber')
                    source_id = source.get('sourceId', '')
                    
                    # Build the citation card HTML
                    card_html = f"""
                    <div class="citation-card">
                        <span class="citation-number">[{idx + 1}]</span>
                        <div class="citation-title">
                    """
                    
                    if url:
                        card_html += f'<a href="{url}" target="_blank" style="color: #1976D2; text-decoration: none;">{title}</a>'
                    else:
                        card_html += f'{title}'
                    
                    card_html += "</div>"
                    
                    # Add excerpt if available
                    if text:
                        max_length = 200
                        display_text = text if len(text) <= max_length else text[:max_length] + "..."
                        card_html += f'<div class="citation-excerpt">"{display_text}"</div>'
                    
                    # Add metadata
                    meta_parts = []
                    if page_number:
                        meta_parts.append(f"📖 Page {page_number}")
                    if source_id:
                        # Truncate long source IDs
                        short_id = source_id[:30] + "..." if len(source_id) > 30 else source_id
                        meta_parts.append(f"ID: {short_id}")
                    
                    if meta_parts:
                        card_html += f'<div class="citation-meta">{" | ".join(meta_parts)}</div>'
                    
                    card_html += "</div>"
                    
                    st.markdown(card_html, unsafe_allow_html=True)

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
    
    # Log what we received
    final_report = result.get("final_report", {})
    sources = final_report.get("sources", [])
    print(f"\n[STREAMLIT] ========== DISPLAYING RESULTS ==========")
    print(f"[STREAMLIT] Sources in final_report: {len(sources)}")
    if sources:
        for i, source in enumerate(sources):
            print(f"[STREAMLIT]   [{i+1}] {source.get('title', 'Untitled')[:50]}")
    else:
        print(f"[STREAMLIT] ⚠️  No sources received from API!")
    print(f"[STREAMLIT] ==========================================\n")
    
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
        # Get sources for adding citation links
        sources = final_report.get("sources", [])
        report_text = final_report.get("synthesized_report", "No report generated")
        
        # Add inline citation badges if sources exist
        if sources:
            report_with_citations = add_citation_links(report_text, sources)
        else:
            report_with_citations = report_text
        
        # Display the synthesized report in an expandable section
        with st.expander("View Complete Report", expanded=True):
            st.markdown(report_with_citations, unsafe_allow_html=True)
    
    # Display sources/citations
    sources = final_report.get("sources", [])
    
    # Debug info (can be removed later)
    with st.expander("🔍 Debug: Source Information", expanded=False):
        st.write(f"**Sources received from API:** {len(sources)}")
        if sources:
            st.write("**Source IDs:**")
            for i, source in enumerate(sources):
                st.write(f"  {i+1}. ID: {source.get('sourceId', 'N/A')}, Title: {source.get('title', 'N/A')}")
        else:
            st.warning("No sources were included in the API response!")
            st.write("**Possible reasons:**")
            st.write("- Stravito API did not return sources")
            st.write("- Sources are in a different field")
            st.write("- Check server logs for details")
    
    if sources:
        st.divider()
        display_sources(sources)
    else:
        st.info("ℹ️ No sources available for this query.")
    
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
                
                # Display sources for this angle if available
                angle_sources = response.get('sources', [])
                if angle_sources:
                    st.write("**Sources for this angle:**")
                    # Display compact source list
                    for j, source in enumerate(angle_sources):
                        source_title = source.get('title', 'Untitled')
                        source_url = source.get('url', '')
                        if source_url:
                            st.markdown(f"- [{j+1}] [{source_title}]({source_url})")
                        else:
                            st.markdown(f"- [{j+1}] {source_title}")
                
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

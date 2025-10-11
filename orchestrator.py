import asyncio
from typing import Dict, Any, List
from openai import AzureOpenAI
from stravito_client import create_conversation, get_message, send_followup, give_feedback
from config import (
    AZURE_OPENAI_API_KEY, 
    AZURE_OPENAI_ENDPOINT, 
    AZURE_OPENAI_API_VERSION, 
    AZURE_OPENAI_DEPLOYMENT_NAME
)

class QueryOrchestrator:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT
        )
        self.deployment_name = AZURE_OPENAI_DEPLOYMENT_NAME

    async def analyze_query_angles(self, query: str) -> List[str]:
        """Generate multiple analysis angles for the query"""
        prompt = f"""
        Given the following query: "{query}"
        
        Generate 3-5 different analytical angles or perspectives to approach this query. 
        Each angle should be a specific, focused question that would provide valuable insights.
        
        Return only the questions, one per line, without numbering or bullet points.
        """
        
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[{"role": "user", "content": prompt}]
        )
        
        angles = [line.strip() for line in response.choices[0].message.content.split('\n') if line.strip()]
        return angles

    async def process_angle(self, angle: str) -> Dict[str, Any]:
        """Process a single analytical angle through Stravito API"""
        try:
            print(f"Processing angle: {angle}")  # Debug log
            
            # Create conversation for this angle
            conversation_response = create_conversation(angle)
            print(f"Conversation response: {conversation_response}")  # Debug log
            
            conversation_id = conversation_response.get('conversationId')
            
            if not conversation_id:
                error_msg = f"Failed to create conversation. Response: {conversation_response}"
                print(f"ERROR: {error_msg}")  # Debug log
                return {"angle": angle, "error": error_msg, "data": None}
            
            # Get the message ID directly from the response
            message_id = conversation_response.get('messageId')
            if not message_id:
                error_msg = f"No message ID found. Response: {conversation_response}"
                print(f"ERROR: {error_msg}")  # Debug log
                return {"angle": angle, "error": error_msg, "data": None}
            
            # Get the full message details
            message_data = get_message(conversation_id, message_id)
            print(f"Message data retrieved for angle: {angle}")  # Debug log
            
            return {
                "angle": angle,
                "conversation_id": conversation_id,
                "message_id": message_id,
                "data": message_data,
                "error": None
            }
            
        except Exception as e:
            error_msg = f"Exception processing angle '{angle}': {str(e)}"
            print(f"EXCEPTION: {error_msg}")  # Debug log
            return {"angle": angle, "error": error_msg, "data": None}

    async def normalize_responses(self, responses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize and clean the responses from different angles"""
        normalized = []
        
        for response in responses:
            if response.get("error"):
                continue
                
            data = response.get("data", {})
            if not data:
                continue
            
            # Extract key information including sources
            normalized_response = {
                "angle": response["angle"],
                "conversation_id": response["conversation_id"],
                "message_id": response["message_id"],
                "content": data.get("content", ""),
                "metadata": data.get("metadata", {}),
                "timestamp": data.get("timestamp", ""),
                "status": data.get("status", ""),
                "sources": data.get("sources", [])  # Extract sources array
            }
            normalized.append(normalized_response)
        
        return normalized

    async def check_contradictions(self, responses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check for contradictions between different angle responses"""
        if len(responses) < 2:
            return responses
        
        # Create a summary of all responses for contradiction analysis
        response_texts = []
        for r in responses:
            response_texts.append(f"Angle: {r['angle']}\nResponse: {r['content']}")
        
        summary_prompt = f"""
        Analyze the following responses for contradictions or conflicting information:
        
        {chr(10).join(response_texts)}
        
        Identify any contradictions or conflicting information between these responses.
        Return a JSON object with:
        - "has_contradictions": boolean
        - "contradictions": list of contradiction descriptions
        - "confidence": confidence level (0-1)
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[{"role": "user", "content": summary_prompt}]
            )
            
            # Parse the response (simplified - in production, use proper JSON parsing)
            analysis = response.choices[0].message.content
            
            # Add contradiction analysis to each response
            for response in responses:
                response["contradiction_analysis"] = analysis
                
        except Exception as e:
            for response in responses:
                response["contradiction_analysis"] = f"Error analyzing contradictions: {str(e)}"
        
        return responses

    async def synthesize_report(self, responses: List[Dict[str, Any]], original_query: str) -> Dict[str, Any]:
        """Synthesize all responses into a comprehensive report"""
        if not responses:
            return {"error": "No valid responses to synthesize"}
        
        # Prepare response texts for synthesis and collect all sources
        response_texts = []
        all_sources = []
        source_map = {}  # To deduplicate sources by sourceId
        
        for r in responses:
            response_texts.append(f"Angle: {r['angle']}\nResponse: {r['content']}")
            # Collect and deduplicate sources
            for source in r.get('sources', []):
                source_id = source.get('sourceId')
                if source_id and source_id not in source_map:
                    source_map[source_id] = source
                    all_sources.append(source)
        
        synthesis_prompt = f"""
        Original Query: "{original_query}"
        
        Based on the following multi-angle analysis, create a comprehensive, structured report:
        
        {chr(10).join(response_texts)}
        
        Create a structured report with:
        1. Executive Summary
        2. Key Findings (organized by theme)
        3. Detailed Analysis
        4. Contradictions or Inconsistencies (if any)
        5. Recommendations or Next Steps
        6. Confidence Assessment
        
        Make the report comprehensive yet concise, and ensure it directly addresses the original query.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[{"role": "user", "content": synthesis_prompt}]
            )
            
            synthesized_report = response.choices[0].message.content
            
            return {
                "original_query": original_query,
                "synthesized_report": synthesized_report,
                "source_angles": [r["angle"] for r in responses],
                "total_angles_processed": len(responses),
                "sources": all_sources,  # Include all collected sources
                "timestamp": asyncio.get_event_loop().time()
            }
            
        except Exception as e:
            return {"error": f"Failed to synthesize report: {str(e)}"}

    async def orchestrate_query(self, query: str) -> Dict[str, Any]:
        """Main orchestration method that handles the entire process"""
        try:
            print(f"Starting orchestration for query: {query}")  # Debug log
            
            # Step 1: Generate multiple analytical angles
            print("Step 1: Generating analytical angles...")  # Debug log
            angles = await self.analyze_query_angles(query)
            print(f"Generated {len(angles)} angles: {angles}")  # Debug log
            
            # Step 2: Process all angles in parallel
            print("Step 2: Processing angles through Stravito API...")  # Debug log
            tasks = [self.process_angle(angle) for angle in angles]
            raw_responses = await asyncio.gather(*tasks, return_exceptions=True)
            print(f"Received {len(raw_responses)} raw responses")  # Debug log
            
            # Filter out exceptions and convert to proper format
            valid_responses = []
            for i, response in enumerate(raw_responses):
                if isinstance(response, Exception):
                    print(f"Response {i} was an exception: {response}")  # Debug log
                    continue
                if response.get("error") is None:
                    valid_responses.append(response)
                    print(f"Response {i} is valid")  # Debug log
                else:
                    print(f"Response {i} has error: {response.get('error')}")  # Debug log
            
            print(f"Valid responses: {len(valid_responses)}")  # Debug log
            
            # Step 3: Normalize responses
            print("Step 3: Normalizing responses...")  # Debug log
            normalized_responses = await self.normalize_responses(valid_responses)
            print(f"Normalized {len(normalized_responses)} responses")  # Debug log
            
            # Step 4: Check for contradictions
            print("Step 4: Checking for contradictions...")  # Debug log
            analyzed_responses = await self.check_contradictions(normalized_responses)
            
            # Step 5: Synthesize final report
            print("Step 5: Synthesizing final report...")  # Debug log
            final_report = await self.synthesize_report(analyzed_responses, query)
            
            print("Orchestration completed successfully")  # Debug log
            return {
                "success": True,
                "original_query": query,
                "angles_generated": angles,
                "responses_processed": len(valid_responses),
                "final_report": final_report,
                "raw_responses": analyzed_responses
            }
            
        except Exception as e:
            print(f"Orchestration failed with exception: {str(e)}")  # Debug log
            return {
                "success": False,
                "error": str(e),
                "original_query": query
            }

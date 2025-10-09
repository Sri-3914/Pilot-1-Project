#!/usr/bin/env python3
"""
Test script to verify the mock orchestrator flow
"""

import asyncio
import json
from mock_orchestrator import MockQueryOrchestrator

async def test_mock_flow():
    """Test the complete mock orchestration flow"""
    print("🧪 Testing Mock Orchestrator Flow")
    print("=" * 50)
    
    # Initialize mock orchestrator
    orchestrator = MockQueryOrchestrator()
    
    # Test queries
    test_queries = [
        "What are the latest trends in AI?",
        "How is climate change affecting global markets?",
        "What are the key challenges in renewable energy adoption?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: {query}")
        print("-" * 40)
        
        try:
            # Run orchestration
            result = await orchestrator.orchestrate_query(query)
            
            # Display results
            if result.get("success"):
                print(f"✅ SUCCESS!")
                print(f"📊 Angles Generated: {len(result.get('angles_generated', []))}")
                print(f"📈 Responses Processed: {result.get('responses_processed', 0)}")
                
                # Show angles
                print(f"\n📝 Generated Angles:")
                for j, angle in enumerate(result.get('angles_generated', []), 1):
                    print(f"  {j}. {angle}")
                
                # Show final report summary
                final_report = result.get('final_report', {})
                if final_report and not final_report.get('error'):
                    report_content = final_report.get('synthesized_report', '')
                    print(f"\n📋 Final Report Preview:")
                    print(f"  Length: {len(report_content)} characters")
                    print(f"  Preview: {report_content[:200]}...")
                else:
                    print(f"❌ Report Error: {final_report.get('error', 'Unknown error')}")
                
            else:
                print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"💥 EXCEPTION: {str(e)}")
        
        print("\n" + "=" * 50)
    
    print("\n🎉 Mock flow testing completed!")

if __name__ == "__main__":
    asyncio.run(test_mock_flow())

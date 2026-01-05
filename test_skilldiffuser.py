"""
Test script for SkillDiffuser functionality.

This script demonstrates the basic usage of SkillDiffuser without making actual API calls.
It shows the data structures and workflow.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.src.skilldiffuser import (
    load_transcriptions_from_file,
    Skill,
    CallAnalysis
)


def test_file_loading():
    """Test loading transcriptions from file."""
    print("="*60)
    print("TEST 1: Loading Transcriptions from File")
    print("="*60)
    
    file_path = "data/transcriptions/example_calls.txt"
    
    if not os.path.exists(file_path):
        print(f"✗ Example file not found: {file_path}")
        return False
    
    calls = load_transcriptions_from_file(file_path)
    
    print(f"✓ Successfully loaded {len(calls)} calls from {file_path}")
    print()
    
    for i, call in enumerate(calls, 1):
        print(f"Call {i}:")
        print(f"  ID: {call['call_id']}")
        print(f"  Transcript length: {len(call['transcript'])} characters")
        print(f"  First 100 chars: {call['transcript'][:100]}...")
        print()
    
    return True


def test_data_structures():
    """Test the data structures used by SkillDiffuser."""
    print("="*60)
    print("TEST 2: Data Structures")
    print("="*60)
    
    # Create example skill
    skill = Skill(
        name="Building Rapport",
        description="Staff uses gratitude to establish positive relationship",
        quote="Thank you for your generous donation of $100 last year",
        timestamp="Line 3",
        effectiveness="high"
    )
    
    print("Example Skill object:")
    print(f"  Name: {skill.name}")
    print(f"  Description: {skill.description}")
    print(f"  Quote: {skill.quote}")
    print(f"  Effectiveness: {skill.effectiveness}")
    print()
    
    # Create example analysis
    analysis = CallAnalysis(
        call_id="CALL_TEST",
        skills=[skill],
        overall_assessment="Effective call with strong rapport building",
        key_insights=[
            "Used gratitude effectively",
            "Created emotional connection"
        ]
    )
    
    print("Example CallAnalysis object:")
    print(f"  Call ID: {analysis.call_id}")
    print(f"  Number of skills: {len(analysis.skills)}")
    print(f"  Overall assessment: {analysis.overall_assessment}")
    print(f"  Key insights: {analysis.key_insights}")
    print()
    
    return True


def test_api_endpoints():
    """Display expected API endpoint formats."""
    print("="*60)
    print("TEST 3: API Endpoint Formats")
    print("="*60)
    
    print("Single Call Analysis Endpoint:")
    print("  POST /analyze_call")
    print()
    print("  Request:")
    print("  {")
    print('    "call_id": "CALL_001",')
    print('    "transcript": "Staff: Hello! ..."')
    print("  }")
    print()
    print("  Response:")
    print("  {")
    print('    "call_id": "CALL_001",')
    print('    "skills": [...]')
    print('    "overall_assessment": "...",')
    print('    "key_insights": [...]')
    print("  }")
    print()
    
    print("Batch Analysis Endpoint:")
    print("  POST /analyze_calls_batch")
    print()
    print("  Request:")
    print("  {")
    print('    "calls": [')
    print('      {"call_id": "CALL_001", "transcript": "..."},')
    print('      {"call_id": "CALL_002", "transcript": "..."}')
    print("    ]")
    print("  }")
    print()
    
    return True


def test_command_line_usage():
    """Display command line usage examples."""
    print("="*60)
    print("TEST 4: Command Line Usage")
    print("="*60)
    
    print("Analyze a single file:")
    print("  python3 analyze_calls.py data/transcriptions/example_calls.txt")
    print()
    
    print("Analyze a directory:")
    print("  python3 analyze_calls.py data/transcriptions/")
    print()
    
    print("Custom output file:")
    print("  python3 analyze_calls.py data/transcriptions/ -o results.json")
    print()
    
    print("Use different model:")
    print("  python3 analyze_calls.py data/transcriptions/ -m gpt-3.5-turbo")
    print()
    
    return True


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("SKILLDIFFUSER TEST SUITE")
    print("="*60)
    print()
    
    tests = [
        ("File Loading", test_file_loading),
        ("Data Structures", test_data_structures),
        ("API Endpoints", test_api_endpoints),
        ("Command Line Usage", test_command_line_usage),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Test '{test_name}' failed with error: {e}")
            results.append((test_name, False))
        print()
    
    # Print summary
    print("="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    total = len(results)
    passed = sum(1 for _, result in results if result)
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    print("="*60)
    
    return all(result for _, result in results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

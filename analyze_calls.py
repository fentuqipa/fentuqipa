"""
Script to load and process donation call transcriptions using SkillDiffuser.

This script can be used to:
1. Load call transcriptions from files
2. Analyze them for skills and persuasion techniques
3. Generate reports and summaries
"""

import os
import sys
import json
import argparse
from dotenv import load_dotenv
from backend.src.skilldiffuser import SkillDiffuser, load_transcriptions_from_file


def load_transcriptions_from_directory(directory_path: str):
    """
    Load all transcription files from a directory.
    
    Args:
        directory_path: Path to directory containing transcription files
        
    Returns:
        List of dictionaries with 'call_id' and 'transcript' keys
    """
    calls = []
    
    if not os.path.exists(directory_path):
        print(f"Error: Directory {directory_path} does not exist")
        return calls
    
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            file_calls = load_transcriptions_from_file(file_path)
            calls.extend(file_calls)
            print(f"Loaded {len(file_calls)} calls from {filename}")
    
    return calls


def save_analysis_to_json(analyses, summary, output_path):
    """
    Save analysis results to a JSON file.
    
    Args:
        analyses: List of CallAnalysis objects
        summary: Summary dictionary from get_skill_summary
        output_path: Path to save the JSON file
    """
    output = {
        "analyses": [
            {
                "call_id": analysis.call_id,
                "skills": [
                    {
                        "name": skill.name,
                        "description": skill.description,
                        "quote": skill.quote,
                        "timestamp": skill.timestamp,
                        "effectiveness": skill.effectiveness
                    }
                    for skill in analysis.skills
                ],
                "overall_assessment": analysis.overall_assessment,
                "key_insights": analysis.key_insights
            }
            for analysis in analyses
        ],
        "summary": summary
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nAnalysis saved to {output_path}")


def print_summary(summary):
    """Print a human-readable summary of the analysis."""
    print("\n" + "="*60)
    print("SKILL ANALYSIS SUMMARY")
    print("="*60)
    print(f"\nTotal Calls Analyzed: {summary['total_calls_analyzed']}")
    print(f"Unique Skills Found: {summary['unique_skills_found']}")
    print("\nSkill Statistics:")
    print("-"*60)
    
    # Sort skills by frequency
    skills_sorted = sorted(
        summary['skill_statistics'].items(),
        key=lambda x: x[1]['frequency'],
        reverse=True
    )
    
    for skill_name, stats in skills_sorted:
        print(f"\n{skill_name}:")
        print(f"  Frequency: {stats['frequency']} times")
        print(f"  Effectiveness Distribution:")
        print(f"    High: {stats['effectiveness_distribution']['high']}")
        print(f"    Medium: {stats['effectiveness_distribution']['medium']}")
        print(f"    Low: {stats['effectiveness_distribution']['low']}")
        print(f"  Avg Effectiveness Score: {stats['avg_effectiveness']:.2f}")
    
    print("\n" + "="*60)


def main():
    """Main function to run the skill diffuser analysis."""
    parser = argparse.ArgumentParser(
        description='Analyze donation call transcriptions to extract skills'
    )
    parser.add_argument(
        'input',
        help='Path to transcription file or directory containing transcription files'
    )
    parser.add_argument(
        '--output',
        '-o',
        default='skill_analysis_results.json',
        help='Output JSON file path (default: skill_analysis_results.json)'
    )
    parser.add_argument(
        '--model',
        '-m',
        default='gpt-4',
        help='OpenAI model to use (default: gpt-4)'
    )
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    api_key = os.environ.get('OPENAI_API_KEY')
    
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please set it in your .env file or as an environment variable")
        sys.exit(1)
    
    # Initialize SkillDiffuser
    print(f"Initializing SkillDiffuser with model: {args.model}")
    diffuser = SkillDiffuser(api_key=api_key, model_name=args.model)
    
    # Load transcriptions
    print(f"\nLoading transcriptions from: {args.input}")
    if os.path.isdir(args.input):
        calls = load_transcriptions_from_directory(args.input)
    elif os.path.isfile(args.input):
        calls = load_transcriptions_from_file(args.input)
    else:
        print(f"Error: {args.input} is not a valid file or directory")
        sys.exit(1)
    
    if not calls:
        print("No calls found to analyze")
        sys.exit(1)
    
    print(f"Found {len(calls)} calls to analyze")
    
    # Analyze calls
    print("\nAnalyzing calls...")
    analyses = []
    for i, call in enumerate(calls, 1):
        print(f"  Analyzing call {i}/{len(calls)}: {call['call_id']}")
        analysis = diffuser.analyze_call(call['call_id'], call['transcript'])
        analyses.append(analysis)
    
    # Generate summary
    print("\nGenerating summary...")
    summary = diffuser.get_skill_summary(analyses)
    
    # Print summary
    print_summary(summary)
    
    # Save results
    save_analysis_to_json(analyses, summary, args.output)
    
    print(f"\n✓ Analysis complete!")


if __name__ == "__main__":
    main()

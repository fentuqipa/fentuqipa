# SkillDiffuser Usage Example

This document demonstrates how to use SkillDiffuser to analyze donation call transcriptions.

## Example 1: Analyze Calls Using Python Script

```python
import os
from dotenv import load_dotenv
from backend.src.skilldiffuser import SkillDiffuser, load_transcriptions_from_file

# Load environment variables
load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')

# Initialize SkillDiffuser
diffuser = SkillDiffuser(api_key=api_key)

# Load calls from file
calls = load_transcriptions_from_file('data/transcriptions/example_calls.txt')
print(f"Loaded {len(calls)} calls")

# Analyze first call
analysis = diffuser.analyze_call(calls[0]['call_id'], calls[0]['transcript'])

# Display results
print(f"\nAnalysis for {analysis.call_id}:")
print(f"Overall Assessment: {analysis.overall_assessment}")
print(f"\nSkills Identified ({len(analysis.skills)}):")
for skill in analysis.skills:
    print(f"\n  • {skill.name} (Effectiveness: {skill.effectiveness})")
    print(f"    Description: {skill.description}")
    print(f"    Quote: \"{skill.quote[:100]}...\"")

print(f"\nKey Insights:")
for insight in analysis.key_insights:
    print(f"  - {insight}")
```

## Example 2: Batch Analysis with Summary

```python
import os
from dotenv import load_dotenv
from backend.src.skilldiffuser import SkillDiffuser, load_transcriptions_from_file

# Setup
load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')
diffuser = SkillDiffuser(api_key=api_key)

# Load and analyze all calls
calls = load_transcriptions_from_file('data/transcriptions/example_calls.txt')
analyses = diffuser.analyze_multiple_calls(calls)

# Generate summary
summary = diffuser.get_skill_summary(analyses)

print(f"Analyzed {summary['total_calls_analyzed']} calls")
print(f"Found {summary['unique_skills_found']} unique skills")
print("\nTop Skills by Frequency:")

# Sort skills by frequency
sorted_skills = sorted(
    summary['skill_statistics'].items(),
    key=lambda x: x[1]['frequency'],
    reverse=True
)

for skill_name, stats in sorted_skills[:5]:  # Top 5
    print(f"\n  {skill_name}:")
    print(f"    Used {stats['frequency']} times")
    print(f"    High effectiveness: {stats['effectiveness_distribution']['high']} times")
```

## Example 3: Using the Command Line Tool

```bash
# Analyze example calls
python3 analyze_calls.py data/transcriptions/example_calls.txt

# This will output:
# - Progress messages showing each call being analyzed
# - A detailed summary of skills found
# - A JSON file (skill_analysis_results.json) with complete results
```

## Example 4: Using the REST API

### Start the server:
```bash
python3 app.py
```

### Analyze a single call:
```bash
curl -X POST http://localhost:5000/analyze_call \
  -H "Content-Type: application/json" \
  -d '{
    "call_id": "CALL_001",
    "transcript": "Staff: Hello! This is Sarah calling from Hope Foundation...\nCustomer: Hi...\n..."
  }'
```

### Analyze multiple calls:
```bash
curl -X POST http://localhost:5000/analyze_calls_batch \
  -H "Content-Type: application/json" \
  -d '{
    "calls": [
      {
        "call_id": "CALL_001",
        "transcript": "Staff: Hello!..."
      },
      {
        "call_id": "CALL_002",
        "transcript": "Staff: Good morning..."
      }
    ]
  }'
```

## Example Output

When you analyze the example calls, you might see results like:

```
============================================================
SKILL ANALYSIS SUMMARY
============================================================

Total Calls Analyzed: 3
Unique Skills Found: 10

Skill Statistics:
------------------------------------------------------------

Gratitude and Recognition:
  Frequency: 3 times
  Effectiveness Distribution:
    High: 3
    Medium: 0
    Low: 0
  Avg Effectiveness Score: 1.00

Creating Urgency:
  Frequency: 3 times
  Effectiveness Distribution:
    High: 2
    Medium: 1
    Low: 0
  Avg Effectiveness Score: 0.67

Social Proof:
  Frequency: 2 times
  Effectiveness Distribution:
    High: 2
    Medium: 0
    Low: 0
  Avg Effectiveness Score: 1.00

Reframing Objections:
  Frequency: 3 times
  Effectiveness Distribution:
    High: 2
    Medium: 1
    Low: 0
  Avg Effectiveness Score: 0.67

...
============================================================
```

## Understanding the Results

### Skill Object Fields

- **name**: The type of skill or technique identified (e.g., "Building Rapport", "Creating Urgency")
- **description**: How the skill was applied in the specific context
- **quote**: The exact text from the transcript demonstrating this skill
- **timestamp**: Where in the call this occurred (if available)
- **effectiveness**: Rating of how well the skill was used (high/medium/low)

### Call Analysis Fields

- **call_id**: Unique identifier for the call
- **skills**: List of all skills identified in the call
- **overall_assessment**: Summary evaluation of the call's effectiveness
- **key_insights**: Important observations about the call strategy

### Summary Statistics

- **total_calls_analyzed**: Number of calls processed
- **unique_skills_found**: Number of distinct skill types identified
- **skill_statistics**: For each skill:
  - **frequency**: How many times it appeared across all calls
  - **effectiveness_distribution**: Breakdown of high/medium/low ratings
  - **avg_effectiveness**: Average effectiveness score (0-1)

## Tips for Best Results

1. **Use clear transcripts**: Make sure speaker labels are consistent (Staff: / Customer:)
2. **Include complete conversations**: Full calls provide better context
3. **Process in batches**: Analyze multiple calls together for better comparative insights
4. **Review the results**: The AI analysis is a tool to augment human judgment, not replace it
5. **Iterate**: Use insights to improve training and call strategies

## Next Steps

After analyzing your calls:

1. **Identify patterns**: Look for skills that appear frequently and are highly effective
2. **Create training materials**: Use successful examples for staff training
3. **Track improvements**: Analyze calls over time to measure progress
4. **Share insights**: Use the summary statistics to inform team meetings and strategy sessions

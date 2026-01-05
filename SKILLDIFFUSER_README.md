# SkillDiffuser for Donation Call Analysis

SkillDiffuser is a tool for analyzing donation call transcriptions to extract and identify persuasion techniques and communication skills used by staff to persuade customers to donate.

## Overview

The SkillDiffuser module uses AI-powered analysis to identify:
- Persuasion techniques (social proof, urgency, reciprocity, etc.)
- Active listening and empathy
- Building rapport and trust
- Handling objections
- Storytelling and emotional appeal
- Clear value proposition
- Closing techniques
- Question framing and discovery

## Installation

The required dependencies are already included in `requirements.txt`. Make sure you have installed them:

```bash
pip install -r requirements.txt
```

## Configuration

Ensure your `.env` file contains your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Method 1: Command Line Script

Use the `analyze_calls.py` script to analyze transcription files:

```bash
# Analyze a single transcription file
python3 analyze_calls.py data/transcriptions/example_calls.txt

# Analyze all transcription files in a directory
python3 analyze_calls.py data/transcriptions/

# Specify custom output file
python3 analyze_calls.py data/transcriptions/ --output results.json

# Use a different model (default is gpt-4)
python3 analyze_calls.py data/transcriptions/ --model gpt-3.5-turbo
```

### Method 2: REST API

Start the Flask application:

```bash
python3 app.py
```

#### Analyze a Single Call

**Endpoint:** `POST /analyze_call`

**Request Body:**
```json
{
  "call_id": "CALL_001",
  "transcript": "Staff: Hello! ... Customer: ..."
}
```

**Example using curl:**
```bash
curl -X POST http://localhost:5000/analyze_call \
  -H "Content-Type: application/json" \
  -d '{
    "call_id": "CALL_001",
    "transcript": "Staff: Hello! This is calling from Hope Foundation..."
  }'
```

**Response:**
```json
{
  "call_id": "CALL_001",
  "skills": [
    {
      "name": "Building Rapport",
      "description": "Staff establishes connection by thanking customer for past support",
      "quote": "Thank you for your generous donation of $100 last year...",
      "timestamp": "",
      "effectiveness": "high"
    }
  ],
  "overall_assessment": "Highly effective call with strong persuasion techniques",
  "key_insights": [
    "Used gratitude to build positive relationship",
    "Created urgency with specific problem statement"
  ]
}
```

#### Analyze Multiple Calls

**Endpoint:** `POST /analyze_calls_batch`

**Request Body:**
```json
{
  "calls": [
    {
      "call_id": "CALL_001",
      "transcript": "Staff: ... Customer: ..."
    },
    {
      "call_id": "CALL_002",
      "transcript": "Staff: ... Customer: ..."
    }
  ]
}
```

**Response:**
```json
{
  "analyses": [
    {
      "call_id": "CALL_001",
      "skills": [...],
      "overall_assessment": "...",
      "key_insights": [...]
    }
  ],
  "summary": {
    "total_calls_analyzed": 2,
    "unique_skills_found": 8,
    "skill_statistics": {
      "Building Rapport": {
        "frequency": 2,
        "effectiveness_distribution": {
          "high": 2,
          "medium": 0,
          "low": 0
        },
        "avg_effectiveness": 1.0
      }
    }
  }
}
```

### Method 3: Python Module

Use SkillDiffuser directly in your Python code:

```python
import os
from dotenv import load_dotenv
from backend.src.skilldiffuser import SkillDiffuser, load_transcriptions_from_file

# Load environment variables
load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')

# Initialize SkillDiffuser
diffuser = SkillDiffuser(api_key=api_key)

# Analyze a single call
transcript = """
Staff: Hello! This is Sarah from Hope Foundation...
Customer: Hi, what's this about?
...
"""

analysis = diffuser.analyze_call("CALL_001", transcript)

# Print results
print(f"Call ID: {analysis.call_id}")
print(f"Skills found: {len(analysis.skills)}")
for skill in analysis.skills:
    print(f"  - {skill.name}: {skill.effectiveness}")

# Analyze multiple calls from a file
calls = load_transcriptions_from_file("data/transcriptions/example_calls.txt")
analyses = diffuser.analyze_multiple_calls(calls)

# Get summary statistics
summary = diffuser.get_skill_summary(analyses)
print(f"Total calls: {summary['total_calls_analyzed']}")
print(f"Unique skills: {summary['unique_skills_found']}")
```

## Transcription File Format

Transcription files should use the following format:

```
---CALL_ID: CALL_001---
Staff: Hello! This is calling from...
Customer: Hi, what's this about?
Staff: ...
---END---

---CALL_ID: CALL_002---
Staff: Good morning...
---END---
```

- Each call starts with `---CALL_ID: <id>---`
- The transcript follows
- Each call ends with `---END---`
- Multiple calls can be in the same file

## Output

The analysis provides:

1. **Skills Identified:** Each skill includes:
   - Name of the skill
   - Description of how it was used
   - Direct quote from the transcript
   - Effectiveness rating (high/medium/low)

2. **Overall Assessment:** A summary of the call's effectiveness

3. **Key Insights:** Important observations about the call

4. **Summary Statistics** (for batch analysis):
   - Total calls analyzed
   - Unique skills found
   - Frequency and effectiveness distribution for each skill

## Example Output

When running the command line script, you'll see output like:

```
============================================================
SKILL ANALYSIS SUMMARY
============================================================

Total Calls Analyzed: 3
Unique Skills Found: 12

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

...
============================================================
```

## Tips for Best Results

1. **Clear Transcripts:** Ensure transcriptions clearly indicate who is speaking (Staff vs. Customer)
2. **Complete Calls:** Include the entire call from greeting to closing
3. **Proper Format:** Follow the file format specification exactly
4. **Model Selection:** Use GPT-4 for better analysis quality (default), or GPT-3.5-turbo for faster/cheaper results
5. **Batch Processing:** For many calls, process them in batches to manage API costs

## Troubleshooting

**Error: "OPENAI_API_KEY not found"**
- Ensure your `.env` file exists and contains the API key
- Make sure the `.env` file is in the project root directory

**Error: "No calls found to analyze"**
- Check that your transcription file follows the correct format
- Verify the file path is correct

**API Rate Limits**
- If you encounter rate limits, try using a smaller batch size or add delays between requests
- Consider using GPT-3.5-turbo instead of GPT-4 for faster processing

## Advanced Usage

### Custom Analysis Prompts

You can extend the `SkillDiffuser` class to customize the analysis:

```python
from backend.src.skilldiffuser import SkillDiffuser

class CustomSkillDiffuser(SkillDiffuser):
    def _create_analysis_prompt(self):
        # Override to add custom instructions
        # Add your specific focus areas or skill categories
        pass
```

### Integrating with Existing Systems

The module can be integrated into existing CRM or analytics systems via the REST API or by importing the Python module directly.

## Support

For issues or questions, please refer to the main project README or open an issue on GitHub.

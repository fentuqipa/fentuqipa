# SkillDiffuser Implementation - Quick Reference

## What is SkillDiffuser?

SkillDiffuser is a tool that uses AI to analyze donation call transcriptions and extract:
- Persuasion techniques used by staff
- Communication skills demonstrated
- Effectiveness ratings for each skill
- Direct quotes showing skill application
- Overall call assessment and insights

## Quick Start

### 1. Setup
```bash
# Install dependencies (already in requirements.txt)
pip install -r requirements.txt

# Set your OpenAI API key in .env file
echo "OPENAI_API_KEY=your_key_here" > .env
```

### 2. Prepare Your Data

Create a transcription file with this format:

```
---CALL_ID: CALL_001---
Staff: Hello, this is calling from...
Customer: Hi, what's this about?
Staff: ...
---END---

---CALL_ID: CALL_002---
Staff: Good morning...
---END---
```

Save to `data/transcriptions/my_calls.txt`

### 3. Analyze Calls

**Option A: Command Line (Recommended for batch processing)**
```bash
python3 analyze_calls.py data/transcriptions/my_calls.txt
```

This creates `skill_analysis_results.json` with complete analysis.

**Option B: REST API (Recommended for integration)**
```bash
# Start server
python3 app.py

# In another terminal
curl -X POST http://localhost:5000/analyze_call \
  -H "Content-Type: application/json" \
  -d '{
    "call_id": "CALL_001",
    "transcript": "Staff: Hello..."
  }'
```

**Option C: Python Code (Recommended for custom workflows)**
```python
from backend.src.skilldiffuser import SkillDiffuser
import os

diffuser = SkillDiffuser(api_key=os.getenv('OPENAI_API_KEY'))
analysis = diffuser.analyze_call("CALL_001", transcript_text)

for skill in analysis.skills:
    print(f"{skill.name}: {skill.effectiveness}")
```

### 4. View Results

Results include:
- **Skills identified** with name, description, quote, and effectiveness
- **Overall assessment** of call effectiveness
- **Key insights** about the call strategy
- **Summary statistics** (for batch analysis)

## Example Output

```
Skill: Gratitude and Recognition
Description: Staff thanks customer for past support to build rapport
Quote: "Thank you for your generous donation of $100 last year..."
Effectiveness: high

Overall Assessment: Highly effective call demonstrating strong 
persuasion techniques and emotional connection.

Key Insights:
- Used gratitude to establish positive relationship
- Created urgency with specific problem statement
- Employed social proof effectively
```

## Files Reference

| File | Purpose |
|------|---------|
| `backend/src/skilldiffuser.py` | Core module |
| `analyze_calls.py` | CLI tool |
| `app.py` | Flask API with endpoints |
| `data/transcriptions/example_calls.txt` | Sample data |
| `SKILLDIFFUSER_README.md` | Full documentation |
| `USAGE_EXAMPLES.md` | Code examples |
| `test_skilldiffuser.py` | Test suite |

## API Endpoints

### POST /analyze_call
Analyze a single call transcription.

**Request:**
```json
{
  "call_id": "CALL_001",
  "transcript": "Staff: Hello..."
}
```

**Response:**
```json
{
  "call_id": "CALL_001",
  "skills": [...],
  "overall_assessment": "...",
  "key_insights": [...]
}
```

### POST /analyze_calls_batch
Analyze multiple calls and get summary statistics.

**Request:**
```json
{
  "calls": [
    {"call_id": "CALL_001", "transcript": "..."},
    {"call_id": "CALL_002", "transcript": "..."}
  ]
}
```

**Response:**
```json
{
  "analyses": [...],
  "summary": {
    "total_calls_analyzed": 2,
    "unique_skills_found": 8,
    "skill_statistics": {...}
  }
}
```

## Common Use Cases

1. **Training Development**: Identify effective techniques for training materials
2. **Performance Review**: Assess staff communication skills objectively
3. **Best Practices**: Find patterns in successful calls
4. **Quality Assurance**: Ensure consistent use of proven techniques
5. **Trend Analysis**: Track skill usage and effectiveness over time

## Troubleshooting

**Error: "OPENAI_API_KEY not found"**
- Create `.env` file with `OPENAI_API_KEY=your_key`

**Error: "No calls found"**
- Check file format matches specification
- Ensure `---CALL_ID:` and `---END---` markers are present

**API Rate Limits**
- Use GPT-3.5-turbo instead of GPT-4: `--model gpt-3.5-turbo`
- Process fewer calls at once

## Next Steps

1. Try the example: `python3 analyze_calls.py data/transcriptions/example_calls.txt`
2. Add your own transcriptions to `data/transcriptions/`
3. Review the generated `skill_analysis_results.json`
4. Use insights to improve training and call strategies

For more details, see `SKILLDIFFUSER_README.md`

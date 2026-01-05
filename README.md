## Step 1. Python Setup

### Option 1: Virtual Environment (Recommended)
1. Create virtual environment
```
python3 -m venv .virtualenv
```

2. Activate the virtual environment
- MacOS
```bash
source .virtualenv/bin/activate
```
- Window
```
.\.virtualenv\Scripts\activate
```

3. Install required packages.

Ensure the virtual environment is activated before installation.

```
pip install -r requirements.txt
```
### Option 2: Install dependencies globally
```
pip install -r requirements.txt
```

## Step 2. SkillDiffuser for Call Analysis

This project includes **SkillDiffuser**, a tool for analyzing donation call transcriptions to extract persuasion techniques and communication skills.

### Quick Start

1. Ensure your `.env` file contains your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

2. Analyze call transcriptions:
```bash
# Using the command line script
python3 analyze_calls.py data/transcriptions/example_calls.txt

# Or start the Flask API
python3 app.py
```

3. View results in the generated JSON file or via API response

For detailed documentation, see [SKILLDIFFUSER_README.md](SKILLDIFFUSER_README.md)

## Step 3. Edit the project

1. Fork the project to your own github repo.
2. Clone the repo to your local site.
3. Modify on the local site.
4. Push the modified code to your github repo.
5. Deploy the branch on Heroku.
   

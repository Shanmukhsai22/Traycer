# Traycer Task Planner

A CLI tool that analyzes your codebase and generates detailed task plans using Google's Gemini AI.

## Features

- 🔍 Intelligent codebase analysis
- 📋 Detailed task planning with AI assistance  
- 🎯 Identifies affected components
- ⏱️ Time estimation
- 🚨 Risk assessment
- 📄 Outputs both Txt and json files

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Shanmukhsai22/Traycer.git
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage

Run from the root directory:

```bash
python -m src.main "your code base path" --task "Your task description"
```

Example:
```bash
python -m src.main "C:\Users\user\Desktop\Project" --task "updating the pagination and ui for resume upload"
```

## Options

- `--task`, `-t`: Task description (required)
- `--output`, `-o`: Output file path (default: plan.txt)

## Output Files

The tool generates two files:

- `plan.txt`
- `plan.json` 

Output includes:
- Task requirements
- Affected components
- Implementation steps
- Time estimates
- Potential risks


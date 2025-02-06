# Traycer Task Planner

A CLI tool that analyzes your codebase and generates detailed task plans using Google's Gemini AI.

## Features

- 🔍 Intelligent codebase analysis
- 📋 Detailed task planning with AI assistance  
- 🎯 Identifies affected components
- ⏱️ Time estimation
- 🚨 Risk assessment
- 📄 Outputs both human-readable (TXT) and machine-readable (JSON) plans

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/traycer.git
cd traycer
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
python traycer.py --task "Your task description"
```

Example:
```bash
python traycer.py --task "Implement user authentication with JWT"
```

## Options

- `--task`, `-t`: Task description (required)
- `--output`, `-o`: Output file path (default: plan.txt)

## Output Files

The tool generates two files:

- `plan.txt`: Human-readable markdown format
- `plan.json`: Machine-readable JSON format

Output includes:
- Task requirements
- Affected components
- Implementation steps
- Time estimates
- Potential risks

## Supported Languages

- Python
- JavaScript/TypeScript
- Java
- C++
- Go
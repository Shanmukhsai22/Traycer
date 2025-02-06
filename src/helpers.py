import os
import json
from typing import List, Dict
from rich.console import Console
from datetime import datetime

console = Console()

def validate_path(path: str) -> bool:
    """Validate if a given path exists."""
    return os.path.exists(path)

def get_file_content(file_path: str) -> str:
    """Read and return file content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        console.print(f"[red]Error reading file {file_path}: {str(e)}[/red]")
        return ""

def get_file_extension(file_path: str) -> str:
    """Get the extension of a file."""
    return os.path.splitext(file_path)[1]

def filter_code_files(files: List[str]) -> List[str]:
    """Filter and return only code files."""
    code_extensions = {'.py', '.cpp', '.h', '.hpp', '.js', '.ts', '.java', '.go'}
    return [f for f in files if get_file_extension(f) in code_extensions]

def create_directory_if_not_exists(path: str) -> None:
    """Create a directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)

def save_plan(plan: Dict, output_path: str) -> None:
    """Save the generated plan to a file."""
    try:
        # Create output directory if needed
        output_dir = os.path.dirname(output_path)
        if output_dir:
            create_directory_if_not_exists(output_dir)

        # Save as markdown file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# Task Plan - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Task Requirements
            f.write("## Requirements\n")
            for req in plan['requirements']:
                f.write(f"- {req}\n")
            f.write("\n")
            
            # Affected Components
            f.write("## Affected Components\n")
            for comp in plan['affected_components']:
                f.write(f"- {comp}\n")
            f.write("\n")
            
            # Implementation Plan
            f.write("## Implementation Plan\n")
            for step in plan['plan']:
                f.write(f"### {step['title']}\n")
                for detail in step['details']:
                    f.write(f"- {detail}\n")
                f.write("\n")
            
            # Time Estimate
            f.write(f"## Estimated Time\n{plan['estimated_time']}\n\n")
            
            # Potential Risks
            f.write("## Potential Risks\n")
            for risk in plan['potential_risks']:
                f.write(f"- {risk}\n")

        # Also save raw JSON for programmatic access
        json_path = f"{os.path.splitext(output_path)[0]}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(plan, f, indent=2)

    except Exception as e:
        raise Exception(f"Error saving plan: {str(e)}")

def format_time_estimate(minutes: int) -> str:
    """Format time estimate in a human-readable format."""
    if minutes < 60:
        return f"{minutes} minutes"
    elif minutes < 1440:  # less than 24 hours
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours} hours{f' {mins} minutes' if mins else ''}"
    else:
        days = minutes // 1440
        hours = (minutes % 1440) // 60
        return f"{days} days{f' {hours} hours' if hours else ''}"
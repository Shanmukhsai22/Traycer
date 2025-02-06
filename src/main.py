import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from .codebase_analyzer import CodebaseAnalyzer
from .task_planner import TaskPlanner
from .ai_engine import AIEngine
from . import helpers

console = Console()

@click.command()
@click.argument('codebase_path', type=click.Path(exists=True))
@click.option('--task', '-t', required=True, help='Task description')
@click.option('--output', '-o', default='plan.txt', help='Output file path')
def main(codebase_path: str, task: str, output: str):
    """Traycer Task Planner - Generate structured plans for coding tasks."""
    try:
        # Display welcome message
        console.print(Panel.fit("🚀 Traycer Task Planner", style="bold blue"))
        
        # Initialize components
        analyzer = CodebaseAnalyzer(codebase_path)
        ai_engine = AIEngine()
        
        # Analyze codebase
        console.print("\n📊 Analyzing codebase...", style="yellow")
        analysis_result = analyzer.analyze()
        
        # Generate plan
        console.print("\n🤖 Generating task plan...", style="yellow")
        planner = TaskPlanner(analysis_result, task, ai_engine)
        plan = planner.generate_plan()
        
        # Save and display results
        helpers.save_plan(plan, output)
        console.print(f"\n✅ Plan generated and saved to: {output}", style="green")
        
        # Display summary
        display_summary(plan)
        
    except Exception as e:
        console.print(f"\n❌ Error: {str(e)}", style="bold red")
        raise click.Abort()

def display_summary(plan: dict):
    """Display a summary of the generated plan."""
    console.print("\n📋 Plan Summary:", style="bold blue")
    
    summary = (
        f"Task Requirements: {len(plan['requirements'])} items\n"
        f"Affected Files: {len(plan['affected_components'])} files\n"
        f"Steps: {len(plan['plan'])} steps\n"
        f"Estimated Time: {plan['estimated_time']}"
    )
    
    console.print(Panel.fit(summary, title="Summary"))

if __name__ == '__main__':
    main()
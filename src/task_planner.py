from typing import Dict, List
from rich.console import Console
from .ai_engine import AIEngine

console = Console()

class TaskPlanner:
    def __init__(self, codebase_analysis: Dict, task_description: str, ai_engine: AIEngine):
        self.analysis = codebase_analysis
        self.task = task_description
        self.ai_engine = ai_engine

    def generate_plan(self) -> Dict:
        """Generate a structured plan based on the task and codebase analysis."""
        console.print("Generating task plan...")

        # Analyze requirements
        requirements = self._analyze_requirements()
        
        # Identify affected components
        affected_components = self._identify_affected_components()
        
        # Generate step-by-step plan
        plan_steps = self._generate_steps()
        
        # Estimate time and risks
        estimated_time = self._estimate_time(plan_steps)
        potential_risks = self._analyze_risks(plan_steps, affected_components)
        
        return {
            'requirements': requirements,
            'affected_components': affected_components,
            'plan': plan_steps,
            'estimated_time': estimated_time,
            'potential_risks': potential_risks
        }

    def _analyze_requirements(self) -> List[str]:
        """Analyze and break down task requirements."""
        prompt = f"""
        Based on the following task, list specific technical requirements and implementation details:
        Task: {self.task}
        
        Format requirements as a bullet list with clear, actionable items.
        Be specific about technical needs and dependencies.
        """
        
        response = self.ai_engine.generate_response(prompt)
        requirements = self._parse_requirements(response)
        
        # Ensure we have at least one requirement
        if not requirements:
            requirements = ["Implement basic project structure"]
            
        return requirements

    def _identify_affected_components(self) -> List[str]:
        """Identify components that need to be modified."""
        prompt = f"""
        Given the task: {self.task}
        
        And the following project structure:
        {self._format_structure(self.analysis['structure'])}
        
        Which files are likely to be affected? List them in order of importance.
        """
        
        response = self.ai_engine.generate_response(prompt)
        return self._parse_affected_files(response)

    def _generate_steps(self) -> List[Dict]:
        """Generate detailed step-by-step plan."""
        prompt = f"""
        Create a detailed step-by-step plan for:
        Task: {self.task}
        
        Consider:
        - Affected files: {', '.join(self._identify_affected_components())}
        - Requirements: {', '.join(self._analyze_requirements())}
        
        For each step, provide:
        1. Clear title
        2. Detailed implementation instructions
        3. Technical considerations
        4. Testing requirements
        """
        
        response = self.ai_engine.generate_response(prompt)
        return self._parse_steps(response)

    def _estimate_time(self, steps: List[Dict]) -> str:
        """Estimate time required for implementation."""
        prompt = f"""
        Estimate the time required to implement:
        Steps: {steps}
        
        Consider:
        - Project size: {self.analysis['summary']['total_lines']} lines
        - Complexity of changes
        - Testing requirements
        
        Provide estimate in format: "X hours" or "X days"
        """
        
        response = self.ai_engine.generate_response(prompt)
        return response.strip()

    def _analyze_risks(self, steps: List[Dict], affected_components: List[str]) -> List[str]:
        """Identify potential risks and challenges."""
        prompt = f"""
        Identify potential risks and challenges for:
        Steps: {steps}
        Affected components: {affected_components}
        
        Consider:
        - Dependencies: {self.analysis['dependencies']}
        - Integration points
        - Potential side effects
        - Performance impacts
        - Security considerations
        """
        
        response = self.ai_engine.generate_response(prompt)
        return self._parse_risks(response)

    def _format_structure(self, structure: Dict, indent: int = 0) -> str:
        """Format project structure for AI prompt."""
        result = []
        for key, value in structure.items():
            if isinstance(value, dict):
                result.append("  " * indent + f"📁 {key}")
                result.append(self._format_structure(value, indent + 1))
            else:
                result.append("  " * indent + f"📄 {key}")
        return "\n".join(result)

    def _parse_requirements(self, response: str) -> List[str]:
        """Parse AI response into requirements list."""
        lines = response.strip().split('\n')
        return [line.strip('- ').strip() for line in lines if line.strip()]

    def _parse_affected_files(self, response: str) -> List[str]:
        """Parse AI response into list of affected files."""
        lines = response.strip().split('\n')
        return [line.strip('- ').strip() for line in lines if line.strip()]

    def _parse_steps(self, response: str) -> List[Dict]:
        """Parse AI response into structured steps."""
        lines = [line for line in response.strip().split('\n') if line.strip()]
        steps = []
        current_step = None
        
        for line in lines:
            if line.startswith(('Step', '#', '1.', '2.', '3.')):
                if current_step and current_step['details']:
                    steps.append(current_step)
                current_step = {'title': line.lstrip('123456789. #'), 'details': []}
            elif current_step:
                current_step['details'].append(line.strip('- '))
                
        if current_step and current_step['details']:
            steps.append(current_step)
            
        # Ensure we have at least one step
        if not steps:
            steps.append({
                'title': 'Initial Setup',
                'details': ['Review requirements and setup project structure']
            })
            
        return steps

    def _parse_risks(self, response: str) -> List[str]:
        """Parse AI response into list of risks."""
        lines = response.strip().split('\n')
        return [line.strip('- ').strip() for line in lines if line.strip()]
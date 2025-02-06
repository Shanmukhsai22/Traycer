import os
from typing import Dict, List
from rich.console import Console
from . import helpers

console = Console()

SUPPORTED_LANGUAGES = {'.py': 'Python', '.cpp': 'C++', '.h': 'C++', '.hpp': 'C++', '.js': 'JavaScript', '.ts': 'TypeScript', '.java': 'Java', '.go': 'Go'}
MAX_FILE_SIZE = 1024 * 1024  # 1MB
IGNORED_DIRS = {'node_modules', '.git', '__pycache__', 'venv', '.env'}

class CodebaseAnalyzer:
    def __init__(self, path: str):
        self.path = path
        self.files = []
        self.structure = {}
        self.dependencies = {}

    def analyze(self) -> Dict:
        """Perform complete analysis of the codebase."""
        console.print("Starting codebase analysis...")
        
        # Scan for files
        self.files = self._scan_files()
        console.print(f"Found {len(self.files)} relevant files")
        
        # Analyze structure
        self.structure = self._analyze_structure()
        
        # Analyze dependencies
        self.dependencies = self._analyze_dependencies()
        
        return {
            'files': self.files,
            'structure': self.structure,
            'dependencies': self.dependencies,
            'summary': self._generate_summary()
        }

    def _scan_files(self) -> List[str]:
        """Scan and return all relevant code files."""
        relevant_files = []
        
        for root, dirs, files in os.walk(self.path):
            # Remove ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            
            for file in files:
                file_path = os.path.join(root, file)
                if self._is_relevant_file(file_path):
                    relevant_files.append(file_path)
                    
        return relevant_files

    def _is_relevant_file(self, file_path: str) -> bool:
        """Check if file is relevant for analysis."""
        ext = helpers.get_file_extension(file_path)
        return (
            ext in SUPPORTED_LANGUAGES and
            os.path.getsize(file_path) <= MAX_FILE_SIZE
        )

    def _analyze_structure(self) -> Dict:
        """Analyze project structure."""
        structure = {}
        
        for file_path in self.files:
            relative_path = os.path.relpath(file_path, self.path)
            parts = relative_path.split(os.sep)
            
            current_dict = structure
            for part in parts[:-1]:
                current_dict = current_dict.setdefault(part, {})
            current_dict[parts[-1]] = self._analyze_file(file_path)
            
        return structure

    def _analyze_file(self, file_path: str) -> Dict:
        """Analyze individual file."""
        content = helpers.get_file_content(file_path)
        return {
            'size': os.path.getsize(file_path),
            'language': SUPPORTED_LANGUAGES[helpers.get_file_extension(file_path)],
            'lines': len(content.splitlines()),
            'imports': self._extract_imports(content, file_path)
        }

    def _analyze_dependencies(self) -> Dict:
        """Analyze project dependencies."""
        dependencies = {}
        
        for file_path in self.files:
            content = helpers.get_file_content(file_path)
            imports = self._extract_imports(content, file_path)
            if imports:
                dependencies[file_path] = imports
                
        return dependencies

    def _extract_imports(self, content: str, file_path: str) -> List[str]:
        """Extract imports/includes from file."""
        ext = helpers.get_file_extension(file_path)
        imports = []
        
        if ext in ['.py']:
            # Python import analysis
            for line in content.splitlines():
                if line.strip().startswith(('import ', 'from ')):
                    imports.append(line.strip())
        elif ext in ['.cpp', '.h', '.hpp']:
            # C++ include analysis
            for line in content.splitlines():
                if line.strip().startswith('#include'):
                    imports.append(line.strip())
                    
        return imports

    def _generate_summary(self) -> Dict:
        """Generate analysis summary."""
        language_stats = {}
        total_lines = 0
        
        for file_path in self.files:
            ext = helpers.get_file_extension(file_path)
            lang = SUPPORTED_LANGUAGES[ext]
            content = helpers.get_file_content(file_path)
            lines = len(content.splitlines())
            
            language_stats[lang] = language_stats.get(lang, 0) + 1
            total_lines += lines
            
        return {
            'total_files': len(self.files),
            'total_lines': total_lines,
            'languages': language_stats
        }
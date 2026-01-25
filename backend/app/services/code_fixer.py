"""
LocalAI Assistant - Code Fixer Service
Automatic code fixing, formatting, and optimization
Author: Manus AI
"""

import ast
import re
from typing import Dict, List, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class CodeFixer:
    """
    Service for automatic code fixing, formatting, and optimization.
    Fixes common issues, formats code, and suggests improvements.
    """
    
    def __init__(self):
        pass
    
    async def fix_code(
        self,
        code: str,
        language: str = "python",
        auto_format: bool = True
    ) -> Dict[str, Any]:
        """
        Fix code issues automatically.
        
        Args:
            code: Source code to fix
            language: Programming language
            auto_format: Whether to auto-format the code
            
        Returns:
            Dictionary with fixed code and changes
        """
        if language.lower() == "python":
            return await self._fix_python(code, auto_format)
        else:
            return await self._fix_generic(code, auto_format)
    
    async def _fix_python(
        self,
        code: str,
        auto_format: bool
    ) -> Dict[str, Any]:
        """Fix Python code"""
        original_code = code
        changes = []
        
        # Fix common issues
        code, common_fixes = await self._fix_common_issues(code)
        changes.extend(common_fixes)
        
        # Fix indentation
        code, indent_fixes = await self._fix_indentation(code)
        changes.extend(indent_fixes)
        
        # Fix imports
        code, import_fixes = await self._fix_imports(code)
        changes.extend(import_fixes)
        
        # Auto-format if requested
        if auto_format:
            code, format_fixes = await self._format_code(code)
            changes.extend(format_fixes)
        
        return {
            "language": "python",
            "original_code": original_code,
            "fixed_code": code,
            "changes": changes,
            "num_changes": len(changes),
            "summary": f"Fixed {len(changes)} issue(s)"
        }
    
    async def _fix_generic(
        self,
        code: str,
        auto_format: bool
    ) -> Dict[str, Any]:
        """Fix generic code"""
        original_code = code
        changes = []
        
        # Basic fixes
        code, basic_fixes = await self._fix_common_issues(code)
        changes.extend(basic_fixes)
        
        return {
            "language": "generic",
            "original_code": original_code,
            "fixed_code": code,
            "changes": changes,
            "num_changes": len(changes),
            "summary": f"Fixed {len(changes)} issue(s)"
        }
    
    async def _fix_common_issues(self, code: str) -> Tuple[str, List[Dict]]:
        """Fix common code issues"""
        changes = []
        lines = code.split("\n")
        fixed_lines = []
        
        for i, line in enumerate(lines, 1):
            original_line = line
            
            # Remove trailing whitespace
            if line.rstrip() != line:
                line = line.rstrip()
                changes.append({
                    "line": i,
                    "type": "trailing_whitespace",
                    "description": "Removed trailing whitespace"
                })
            
            # Fix multiple spaces to single space (except indentation)
            stripped = line.lstrip()
            indent = line[:len(line) - len(stripped)]
            if "  " in stripped and not stripped.startswith("#"):
                fixed_stripped = re.sub(r"  +", " ", stripped)
                line = indent + fixed_stripped
                if line != original_line:
                    changes.append({
                        "line": i,
                        "type": "multiple_spaces",
                        "description": "Fixed multiple spaces"
                    })
            
            # Fix missing spaces around operators
            if "=" in line and not line.strip().startswith("#"):
                # Don't fix in strings
                if "\"" not in line and "'" not in line:
                    original = line
                    line = re.sub(r"([^\s=!<>])=([^\s=])", r"\1 = \2", line)
                    if line != original:
                        changes.append({
                            "line": i,
                            "type": "operator_spacing",
                            "description": "Fixed spacing around operators"
                        })
            
            fixed_lines.append(line)
        
        return "\n".join(fixed_lines), changes
    
    async def _fix_indentation(self, code: str) -> Tuple[str, List[Dict]]:
        """Fix indentation issues"""
        changes = []
        lines = code.split("\n")
        fixed_lines = []
        
        for i, line in enumerate(lines, 1):
            if not line.strip():
                fixed_lines.append("")
                continue
            
            # Count leading spaces
            indent = len(line) - len(line.lstrip())
            
            # Check if indentation is multiple of 4
            if indent > 0 and indent % 4 != 0:
                # Round to nearest multiple of 4
                new_indent = (indent + 2) // 4 * 4
                new_line = " " * new_indent + line.lstrip()
                fixed_lines.append(new_line)
                changes.append({
                    "line": i,
                    "type": "indentation",
                    "description": f"Fixed indentation from {indent} to {new_indent} spaces"
                })
            else:
                fixed_lines.append(line)
        
        return "\n".join(fixed_lines), changes
    
    async def _fix_imports(self, code: str) -> Tuple[str, List[Dict]]:
        """Fix import issues"""
        changes = []
        lines = code.split("\n")
        fixed_lines = []
        imports = {}
        import_lines = []
        
        # Collect imports
        for i, line in enumerate(lines, 1):
            if line.strip().startswith("import ") or line.strip().startswith("from "):
                import_lines.append((i, line))
            else:
                fixed_lines.append(line)
        
        # Sort imports
        import_lines.sort(key=lambda x: x[1])
        
        # Add sorted imports back
        if import_lines:
            for i, (orig_line_num, line) in enumerate(import_lines):
                if i == 0:
                    fixed_lines.insert(0, line)
                else:
                    fixed_lines.insert(i, line)
        
        return "\n".join(fixed_lines), changes
    
    async def _format_code(self, code: str) -> Tuple[str, List[Dict]]:
        """Format code according to style guidelines"""
        changes = []
        lines = code.split("\n")
        fixed_lines = []
        
        for i, line in enumerate(lines, 1):
            original_line = line
            
            # Ensure 2 blank lines before class/function definitions (except first)
            if i > 1 and (line.strip().startswith("def ") or line.strip().startswith("class ")):
                if i >= 2 and fixed_lines[-1].strip() != "":
                    fixed_lines.append("")
                    if i >= 3 and fixed_lines[-2].strip() != "":
                        fixed_lines.insert(-1, "")
                        changes.append({
                            "line": i,
                            "type": "formatting",
                            "description": "Added blank lines before definition"
                        })
            
            fixed_lines.append(line)
        
        return "\n".join(fixed_lines), changes
    
    async def optimize_code(self, code: str) -> Dict[str, Any]:
        """
        Suggest code optimizations.
        
        Args:
            code: Source code to optimize
            
        Returns:
            Dictionary with optimization suggestions
        """
        suggestions = []
        
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {
                "error": "Syntax error in code",
                "suggestions": []
            }
        
        # Check for optimization opportunities
        for node in ast.walk(tree):
            # Suggest list comprehension instead of loop
            if isinstance(node, ast.For):
                if isinstance(node.body[0], ast.Expr):
                    if isinstance(node.body[0].value, ast.Call):
                        suggestions.append({
                            "line": node.lineno,
                            "type": "list_comprehension",
                            "message": "Consider using list comprehension instead of for loop",
                            "severity": "info"
                        })
            
            # Suggest generator instead of list for large iterations
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id == "list":
                        suggestions.append({
                            "line": node.lineno,
                            "type": "generator",
                            "message": "Consider using a generator instead of list() for memory efficiency",
                            "severity": "info"
                        })
        
        return {
            "suggestions": suggestions,
            "num_suggestions": len(suggestions),
            "summary": f"Found {len(suggestions)} optimization opportunity(ies)"
        }
    
    async def explain_code(self, code: str) -> Dict[str, Any]:
        """
        Generate explanation of code.
        
        Args:
            code: Source code to explain
            
        Returns:
            Dictionary with code explanation
        """
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {
                "error": f"Syntax error: {e.msg}",
                "explanation": None
            }
        
        explanation = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                explanation.append({
                    "type": "function",
                    "name": node.name,
                    "line": node.lineno,
                    "description": f"Function '{node.name}' defined",
                    "args": [arg.arg for arg in node.args.args],
                    "docstring": ast.get_docstring(node)
                })
            elif isinstance(node, ast.ClassDef):
                explanation.append({
                    "type": "class",
                    "name": node.name,
                    "line": node.lineno,
                    "description": f"Class '{node.name}' defined",
                    "docstring": ast.get_docstring(node)
                })
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    explanation.append({
                        "type": "import",
                        "module": alias.name,
                        "line": node.lineno,
                        "description": f"Imports module '{alias.name}'"
                    })
        
        return {
            "explanation": explanation,
            "num_items": len(explanation),
            "summary": f"Code contains {len([e for e in explanation if e['type'] == 'function'])} function(s) "
                      f"and {len([e for e in explanation if e['type'] == 'class'])} class(es)"
        }


# Global instance
code_fixer = CodeFixer()

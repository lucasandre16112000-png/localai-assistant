"""
LocalAI Assistant - Code Analyzer Service
Advanced code analysis, quality checking, and issue detection
Author: Manus AI
"""

import ast
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class CodeIssue:
    """Represents a code issue"""
    line: int
    column: int
    severity: str  # error, warning, info
    message: str
    code: str
    suggestion: Optional[str] = None


class CodeAnalyzer:
    """
    Comprehensive code analysis service.
    Analyzes code for syntax errors, complexity, quality, security issues, and best practices.
    """
    
    def __init__(self):
        self.max_complexity = 10
        self.max_line_length = 120
        self.max_function_length = 50
    
    async def analyze_code(
        self,
        code: str,
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        Perform comprehensive code analysis.
        
        Args:
            code: Source code to analyze
            language: Programming language (python, javascript, etc)
            
        Returns:
            Dictionary with analysis results
        """
        if language.lower() == "python":
            return await self._analyze_python(code)
        else:
            return await self._analyze_generic(code)
    
    async def _analyze_python(self, code: str) -> Dict[str, Any]:
        """Analyze Python code"""
        issues = []
        
        # Syntax check
        syntax_issues = await self._check_syntax(code)
        issues.extend(syntax_issues)
        
        if syntax_issues:
            # Can't analyze further if there are syntax errors
            return {
                "language": "python",
                "has_errors": True,
                "issues": [self._issue_to_dict(issue) for issue in issues],
                "summary": f"Found {len(issues)} syntax error(s)"
            }
        
        # Parse the AST
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {
                "language": "python",
                "has_errors": True,
                "issues": [{
                    "line": e.lineno or 0,
                    "column": e.offset or 0,
                    "severity": "error",
                    "message": e.msg,
                    "code": "E001"
                }],
                "summary": "Syntax error"
            }
        
        # Complexity analysis
        complexity_issues = await self._analyze_complexity(tree, code)
        issues.extend(complexity_issues)
        
        # Code style issues
        style_issues = await self._check_code_style(code)
        issues.extend(style_issues)
        
        # Security issues
        security_issues = await self._check_security(tree, code)
        issues.extend(security_issues)
        
        # Best practices
        practice_issues = await self._check_best_practices(tree, code)
        issues.extend(practice_issues)
        
        # Metrics
        metrics = await self._calculate_metrics(tree, code)
        
        return {
            "language": "python",
            "has_errors": any(issue.severity == "error" for issue in issues),
            "issues": [self._issue_to_dict(issue) for issue in sorted(
                issues, key=lambda x: (x.line, x.column)
            )],
            "metrics": metrics,
            "summary": f"Found {len(issues)} issue(s): "
                      f"{sum(1 for i in issues if i.severity == 'error')} error(s), "
                      f"{sum(1 for i in issues if i.severity == 'warning')} warning(s), "
                      f"{sum(1 for i in issues if i.severity == 'info')} info(s)"
        }
    
    async def _analyze_generic(self, code: str) -> Dict[str, Any]:
        """Generic code analysis for non-Python languages"""
        issues = []
        
        # Basic checks
        lines = code.split("\n")
        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > self.max_line_length:
                issues.append(CodeIssue(
                    line=i,
                    column=self.max_line_length,
                    severity="warning",
                    message=f"Line too long ({len(line)} > {self.max_line_length})",
                    code="W001"
                ))
            
            # Check for TODO/FIXME comments
            if "TODO" in line or "FIXME" in line:
                issues.append(CodeIssue(
                    line=i,
                    column=line.find("TODO" if "TODO" in line else "FIXME"),
                    severity="info",
                    message="TODO/FIXME comment found",
                    code="I001"
                ))
        
        return {
            "language": "generic",
            "has_errors": False,
            "issues": [self._issue_to_dict(issue) for issue in issues],
            "summary": f"Found {len(issues)} issue(s)"
        }
    
    async def _check_syntax(self, code: str) -> List[CodeIssue]:
        """Check for syntax errors"""
        issues = []
        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append(CodeIssue(
                line=e.lineno or 0,
                column=e.offset or 0,
                severity="error",
                message=e.msg,
                code="E001"
            ))
        except Exception as e:
            issues.append(CodeIssue(
                line=0,
                column=0,
                severity="error",
                message=str(e),
                code="E002"
            ))
        return issues
    
    async def _analyze_complexity(
        self,
        tree: ast.AST,
        code: str
    ) -> List[CodeIssue]:
        """Analyze code complexity"""
        issues = []
        lines = code.split("\n")
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Calculate cyclomatic complexity
                complexity = self._calculate_cyclomatic_complexity(node)
                
                if complexity > self.max_complexity:
                    issues.append(CodeIssue(
                        line=node.lineno,
                        column=0,
                        severity="warning",
                        message=f"Function '{node.name}' has high complexity ({complexity})",
                        code="C001",
                        suggestion=f"Consider breaking down this function (complexity: {complexity})"
                    ))
                
                # Check function length
                func_length = node.end_lineno - node.lineno if node.end_lineno else 0
                if func_length > self.max_function_length:
                    issues.append(CodeIssue(
                        line=node.lineno,
                        column=0,
                        severity="warning",
                        message=f"Function '{node.name}' is too long ({func_length} lines)",
                        code="C002",
                        suggestion=f"Consider breaking down this function"
                    ))
        
        return issues
    
    async def _check_code_style(self, code: str) -> List[CodeIssue]:
        """Check code style issues"""
        issues = []
        lines = code.split("\n")
        
        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > self.max_line_length:
                issues.append(CodeIssue(
                    line=i,
                    column=self.max_line_length,
                    severity="warning",
                    message=f"Line too long ({len(line)} > {self.max_line_length})",
                    code="W001"
                ))
            
            # Check for trailing whitespace
            if line.rstrip() != line:
                issues.append(CodeIssue(
                    line=i,
                    column=len(line.rstrip()),
                    severity="info",
                    message="Trailing whitespace",
                    code="I002"
                ))
            
            # Check for multiple statements on one line
            if ";" in line and not line.strip().startswith("#"):
                issues.append(CodeIssue(
                    line=i,
                    column=line.find(";"),
                    severity="warning",
                    message="Multiple statements on one line",
                    code="W002"
                ))
        
        return issues
    
    async def _check_security(
        self,
        tree: ast.AST,
        code: str
    ) -> List[CodeIssue]:
        """Check for security issues"""
        issues = []
        
        for node in ast.walk(tree):
            # Check for eval/exec
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ["eval", "exec", "compile"]:
                        issues.append(CodeIssue(
                            line=node.lineno,
                            column=node.col_offset,
                            severity="error",
                            message=f"Dangerous function '{node.func.id}' used",
                            code="S001",
                            suggestion=f"Avoid using {node.func.id}() - it's a security risk"
                        ))
            
            # Check for hardcoded passwords/secrets
            if isinstance(node, ast.Constant):
                if isinstance(node.value, str):
                    if any(keyword in node.value.lower() for keyword in ["password", "secret", "api_key", "token"]):
                        if len(node.value) > 10:
                            issues.append(CodeIssue(
                                line=node.lineno,
                                column=node.col_offset,
                                severity="warning",
                                message="Possible hardcoded secret detected",
                                code="S002",
                                suggestion="Use environment variables for secrets"
                            ))
        
        return issues
    
    async def _check_best_practices(
        self,
        tree: ast.AST,
        code: str
    ) -> List[CodeIssue]:
        """Check for best practice violations"""
        issues = []
        
        for node in ast.walk(tree):
            # Check for bare except
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    issues.append(CodeIssue(
                        line=node.lineno,
                        column=node.col_offset,
                        severity="warning",
                        message="Bare except clause",
                        code="B001",
                        suggestion="Specify the exception type to catch"
                    ))
            
            # Check for mutable default arguments
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for default in node.args.defaults:
                    if isinstance(default, (ast.List, ast.Dict)):
                        issues.append(CodeIssue(
                            line=node.lineno,
                            column=node.col_offset,
                            severity="warning",
                            message=f"Mutable default argument in function '{node.name}'",
                            code="B002",
                            suggestion="Use None as default and initialize inside the function"
                        ))
        
        return issues
    
    def _calculate_cyclomatic_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity of a function"""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity
    
    async def _calculate_metrics(
        self,
        tree: ast.AST,
        code: str
    ) -> Dict[str, Any]:
        """Calculate code metrics"""
        lines = code.split("\n")
        
        metrics = {
            "total_lines": len(lines),
            "code_lines": len([l for l in lines if l.strip() and not l.strip().startswith("#")]),
            "comment_lines": len([l for l in lines if l.strip().startswith("#")]),
            "blank_lines": len([l for l in lines if not l.strip()]),
            "functions": 0,
            "classes": 0,
            "imports": 0,
            "avg_line_length": sum(len(l) for l in lines) // len(lines) if lines else 0
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                metrics["functions"] += 1
            elif isinstance(node, ast.ClassDef):
                metrics["classes"] += 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                metrics["imports"] += 1
        
        return metrics
    
    def _issue_to_dict(self, issue: CodeIssue) -> Dict[str, Any]:
        """Convert CodeIssue to dictionary"""
        return {
            "line": issue.line,
            "column": issue.column,
            "severity": issue.severity,
            "message": issue.message,
            "code": issue.code,
            "suggestion": issue.suggestion
        }


# Global instance
code_analyzer = CodeAnalyzer()

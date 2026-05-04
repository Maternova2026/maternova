import ast
import json

class InternalComplexityAnalyzer:
    """
    Analyzes internal software complexity metrics such as McCabe's Cyclomatic Complexity.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.code = self._read_file()
        self.tree = ast.parse(self.code)

    def _read_file(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def compute_cyclomatic_complexity(self, node):
        """
        Computes McCabe's Cyclomatic Complexity for a given AST node.
        Base complexity is 1. We add 1 for each control flow branch.
        """
        complexity = 1
        for child in ast.walk(node):
            # Control flow statements that add branches
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler, ast.With)):
                complexity += 1
            # Boolean operators (and, or) also add to complexity
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            # Python 3.10+ Match statement
            elif hasattr(ast, 'Match') and isinstance(child, getattr(ast, 'Match')):
                complexity += len(child.cases)
        return complexity

    def analyze(self):
        functions = [n for n in ast.walk(self.tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        classes = [n for n in ast.walk(self.tree) if isinstance(n, ast.ClassDef)]
        
        total_complexity = self.compute_cyclomatic_complexity(self.tree)
        
        func_complexities = []
        for func in functions:
            comp = self.compute_cyclomatic_complexity(func)
            func_complexities.append({
                "name": func.name,
                "complexity": comp
            })
            
        avg_complexity = sum(f["complexity"] for f in func_complexities) / len(functions) if functions else 0
        
        return {
            "Total Cyclomatic Complexity": total_complexity,
            "Total Functions": len(functions),
            "Total Classes": len(classes),
            "Average Complexity per Function": round(avg_complexity, 2),
            "Functions Breakdown": func_complexities
        }

if __name__ == "__main__":
    analyzer = InternalComplexityAnalyzer("app.py")
    results = analyzer.analyze()

    print("\n=== INTERNAL SOFTWARE COMPLEXITY ANALYSIS ===\n")
    print(f"Total Cyclomatic Complexity: {results['Total Cyclomatic Complexity']}")
    print(f"Total Functions: {results['Total Functions']}")
    print(f"Total Classes: {results['Total Classes']}")
    print(f"Average Complexity per Function: {results['Average Complexity per Function']}")
    
    print("\nTop 5 Most Complex Functions:")
    sorted_funcs = sorted(results["Functions Breakdown"], key=lambda x: x["complexity"], reverse=True)
    for f in sorted_funcs[:5]:
        print(f" - {f['name']}: {f['complexity']}")

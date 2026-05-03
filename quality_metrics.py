"""
quality_metrics.py - Software Quality Metrics for the MATERNOVA Project
========================================================================

Chapter 8 Implementation: Measuring External Software Metrics - Quality
Implements ISO 9126 quality model with external metrics for:
- Functionality
- Reliability  
- Usability
- Efficiency
- Maintainability
- Portability

Course: SENG 421 – Software Metrics (Chapter 8)
System: Maternova – Maternal Health Management System
"""

import os
import re
import time
import json
import subprocess
import sys
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class QualityMetric:
    """Represents a single quality metric with its measurement"""
    name: str
    value: float
    unit: str
    description: str
    target: Optional[float] = None
    status: str = "unknown"  # excellent, good, average, poor


@dataclass
class QualityCharacteristic:
    """Represents a quality characteristic from ISO 9126"""
    name: str
    description: str
    metrics: List[QualityMetric] = field(default_factory=list)
    weight: float = 1.0
    
    def add_metric(self, metric: QualityMetric):
        """Add a metric to this characteristic"""
        self.metrics.append(metric)
    
    def calculate_score(self) -> float:
        """Calculate weighted average score for this characteristic"""
        if not self.metrics:
            return 0.0
        
        total_score = 0.0
        total_weight = 0.0
        
        for metric in self.metrics:
            # Normalize metric value to 0-100 scale
            normalized = self._normalize_metric(metric)
            metric_weight = 1.0  # Equal weighting for now
            total_score += normalized * metric_weight
            total_weight += metric_weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def _normalize_metric(self, metric: QualityMetric) -> float:
        """Normalize metric value to 0-100 scale"""
        if metric.target:
            # If target exists, calculate percentage of target
            return min(100.0, (metric.value / metric.target) * 100)
        else:
            # Otherwise use industry benchmarks
            return self._benchmark_normalize(metric)
    
    def _benchmark_normalize(self, metric: QualityMetric) -> float:
        """Normalize using industry benchmarks"""
        benchmarks = {
            # Functionality benchmarks
            "function_coverage": 80.0,
            "api_completeness": 90.0,
            
            # Reliability benchmarks  
            "mtbf": 168.0,  # hours
            "defect_density": 1.0,  # defects per KLOC
            "uptime": 99.5,  # percentage
            
            # Usability benchmarks
            "task_completion_rate": 95.0,
            "user_error_rate": 5.0,
            "learnability_time": 30.0,  # minutes
            
            # Efficiency benchmarks
            "response_time": 2.0,  # seconds
            "throughput": 100.0,  # requests per second
            "memory_usage": 100.0,  # MB
            
            # Maintainability benchmarks
            "cyclomatic_complexity": 10.0,
            "comment_ratio": 20.0,  # percentage
            "modularity": 0.8,  # ratio
            
            # Portability benchmarks
            "platform_compatibility": 3.0,  # number of platforms
            "deployment_time": 10.0,  # minutes
        }
        
        benchmark = benchmarks.get(metric.name.lower(), 50.0)
        
        # For metrics where lower is better (like error rates, complexity)
        lower_is_better = ["defect_density", "user_error_rate", "cyclomatic_complexity", 
                          "response_time", "memory_usage", "learnability_time"]
        
        if metric.name.lower() in lower_is_better:
            return max(0.0, 100.0 - (metric.value / benchmark) * 100)
        else:
            return min(100.0, (metric.value / benchmark) * 100)


class QualityMetricsAnalyzer:
    """
    Main analyzer for software quality metrics based on ISO 9126
    """
    
    def __init__(self, project_path: str = "."):
        self.project_path = project_path
        self.characteristics = {}
        self.analysis_date = datetime.now()
        self._initialize_characteristics()
    
    def _initialize_characteristics(self):
        """Initialize ISO 9126 quality characteristics"""
        self.characteristics = {
            "Functionality": QualityCharacteristic(
                "Functionality",
                "The set of attributes that bear on the existence of a set of functions and their specified properties"
            ),
            "Reliability": QualityCharacteristic(
                "Reliability", 
                "The capability of software to maintain its level of performance under stated conditions for a stated period of time"
            ),
            "Usability": QualityCharacteristic(
                "Usability",
                "The effort needed for use, and on the individual assessment of such use, by a stated or implied set of users"
            ),
            "Efficiency": QualityCharacteristic(
                "Efficiency",
                "The relationship between the level of performance of the software and the amount of resources used"
            ),
            "Maintainability": QualityCharacteristic(
                "Maintainability",
                "The effort needed to make specified modifications"
            ),
            "Portability": QualityCharacteristic(
                "Portability",
                "The ability of software to be transferred from one environment to another"
            )
        }
    
    def analyze_functionality(self) -> Dict[str, float]:
        """Analyze functionality metrics"""
        print("Analyzing Functionality Metrics...")
        
        # Function coverage analysis
        coverage_result = self._analyze_code_coverage()
        coverage_metric = QualityMetric(
            "function_coverage",
            coverage_result["coverage_percentage"],
            "%",
            "Percentage of functions with test coverage",
            target=80.0
        )
        
        # API completeness
        api_completeness = self._analyze_api_completeness()
        api_metric = QualityMetric(
            "api_completeness",
            api_completeness,
            "%",
            "Percentage of required API endpoints implemented",
            target=90.0
        )
        
        # Input validation coverage
        validation_score = self._analyze_input_validation()
        validation_metric = QualityMetric(
            "input_validation",
            validation_score,
            "%",
            "Percentage of inputs with proper validation",
            target=95.0
        )
        
        # Add metrics to characteristic
        self.characteristics["Functionality"].add_metric(coverage_metric)
        self.characteristics["Functionality"].add_metric(api_metric)
        self.characteristics["Functionality"].add_metric(validation_metric)
        
        return {
            "function_coverage": coverage_result["coverage_percentage"],
            "api_completeness": api_completeness,
            "input_validation": validation_score
        }
    
    def analyze_reliability(self) -> Dict[str, float]:
        """Analyze reliability metrics"""
        print("Analyzing Reliability Metrics...")
        
        # Defect density (simulated based on code analysis)
        defect_density = self._calculate_defect_density()
        defect_metric = QualityMetric(
            "defect_density",
            defect_density,
            "defects/KLOC",
            "Number of defects per thousand lines of code",
            target=1.0
        )
        
        # Error handling coverage
        error_handling = self._analyze_error_handling()
        error_metric = QualityMetric(
            "error_handling_coverage",
            error_handling,
            "%",
            "Percentage of functions with proper error handling",
            target=85.0
        )
        
        # Code stability (based on complexity)
        stability_score = self._analyze_code_stability()
        stability_metric = QualityMetric(
            "code_stability",
            stability_score,
            "score",
            "Code stability score based on complexity and structure",
            target=80.0
        )
        
        # Add metrics to characteristic
        self.characteristics["Reliability"].add_metric(defect_metric)
        self.characteristics["Reliability"].add_metric(error_metric)
        self.characteristics["Reliability"].add_metric(stability_metric)
        
        return {
            "defect_density": defect_density,
            "error_handling_coverage": error_handling,
            "code_stability": stability_score
        }
    
    def analyze_usability(self) -> Dict[str, float]:
        """Analyze usability metrics"""
        print("Analyzing Usability Metrics...")
        
        # UI consistency (based on template patterns)
        ui_consistency = self._analyze_ui_consistency()
        ui_metric = QualityMetric(
            "ui_consistency",
            ui_consistency,
            "%",
            "Percentage of consistent UI elements",
            target=90.0
        )
        
        # Navigation complexity
        nav_complexity = self._analyze_navigation_complexity()
        nav_metric = QualityMetric(
            "navigation_complexity",
            nav_complexity,
            "score",
            "Navigation complexity score (lower is better)",
            target=5.0
        )
        
        # Form validation feedback
        form_feedback = self._analyze_form_feedback()
        form_metric = QualityMetric(
            "form_feedback_quality",
            form_feedback,
            "%",
            "Quality of form validation feedback",
            target=85.0
        )
        
        # Add metrics to characteristic
        self.characteristics["Usability"].add_metric(ui_metric)
        self.characteristics["Usability"].add_metric(nav_metric)
        self.characteristics["Usability"].add_metric(form_metric)
        
        return {
            "ui_consistency": ui_consistency,
            "navigation_complexity": nav_complexity,
            "form_feedback_quality": form_feedback
        }
    
    def analyze_efficiency(self) -> Dict[str, float]:
        """Analyze efficiency metrics"""
        print("Analyzing Efficiency Metrics...")
        
        # Code efficiency (based on algorithms and data structures)
        code_efficiency = self._analyze_code_efficiency()
        efficiency_metric = QualityMetric(
            "code_efficiency",
            code_efficiency,
            "score",
            "Code efficiency score based on algorithmic complexity",
            target=75.0
        )
        
        # Database query optimization
        db_optimization = self._analyze_database_efficiency()
        db_metric = QualityMetric(
            "database_efficiency",
            db_optimization,
            "%",
            "Percentage of optimized database queries",
            target=80.0
        )
        
        # Resource usage patterns
        resource_usage = self._analyze_resource_usage()
        resource_metric = QualityMetric(
            "resource_efficiency",
            resource_usage,
            "score",
            "Resource usage efficiency score",
            target=70.0
        )
        
        # Add metrics to characteristic
        self.characteristics["Efficiency"].add_metric(efficiency_metric)
        self.characteristics["Efficiency"].add_metric(db_metric)
        self.characteristics["Efficiency"].add_metric(resource_metric)
        
        return {
            "code_efficiency": code_efficiency,
            "database_efficiency": db_optimization,
            "resource_efficiency": resource_usage
        }
    
    def analyze_maintainability(self) -> Dict[str, float]:
        """Analyze maintainability metrics"""
        print("Analyzing Maintainability Metrics...")
        
        # Code structure analysis
        structure_score = self._analyze_code_structure()
        structure_metric = QualityMetric(
            "code_structure",
            structure_score,
            "score",
            "Code structure quality score",
            target=80.0
        )
        
        # Documentation quality
        doc_quality = self._analyze_documentation_quality()
        doc_metric = QualityMetric(
            "documentation_quality",
            doc_quality,
            "%",
            "Percentage of well-documented functions",
            target=70.0
        )
        
        # Modularity assessment
        modularity_score = self._analyze_modularity()
        mod_metric = QualityMetric(
            "modularity",
            modularity_score,
            "score",
            "Code modularity score",
            target=75.0
        )
        
        # Add metrics to characteristic
        self.characteristics["Maintainability"].add_metric(structure_metric)
        self.characteristics["Maintainability"].add_metric(doc_metric)
        self.characteristics["Maintainability"].add_metric(mod_metric)
        
        return {
            "code_structure": structure_score,
            "documentation_quality": doc_quality,
            "modularity": modularity_score
        }
    
    def analyze_portability(self) -> Dict[str, float]:
        """Analyze portability metrics"""
        print("Analyzing Portability Metrics...")
        
        # Platform independence
        platform_score = self._analyze_platform_independence()
        platform_metric = QualityMetric(
            "platform_independence",
            platform_score,
            "score",
            "Platform independence score",
            target=70.0
        )
        
        # Configuration management
        config_score = self._analyze_configuration_management()
        config_metric = QualityMetric(
            "configuration_management",
            config_score,
            "%",
            "Percentage of externalized configuration",
            target=85.0
        )
        
        # Dependency management
        dependency_score = self._analyze_dependency_management()
        dep_metric = QualityMetric(
            "dependency_management",
            dependency_score,
            "score",
            "Dependency management quality",
            target=75.0
        )
        
        # Add metrics to characteristic
        self.characteristics["Portability"].add_metric(platform_metric)
        self.characteristics["Portability"].add_metric(config_metric)
        self.characteristics["Portability"].add_metric(dep_metric)
        
        return {
            "platform_independence": platform_score,
            "configuration_management": config_score,
            "dependency_management": dependency_score
        }
    
    # Helper methods for metric calculations
    
    def _analyze_code_coverage(self) -> Dict[str, float]:
        """Analyze code coverage (simulated)"""
        # In a real implementation, this would run coverage tools
        # For now, we'll simulate based on test file analysis
        test_files = ["test_metrics.py"]
        main_files = ["app.py", "software_size.py", "cost_metrics.py"]
        
        estimated_coverage = 65.0  # Conservative estimate based on existing tests
        
        return {
            "coverage_percentage": estimated_coverage,
            "lines_covered": int(estimated_coverage * 0.65),  # Based on app.py LOC
            "total_lines": 2967
        }
    
    def _analyze_api_completeness(self) -> float:
        """Analyze API completeness for Flask application"""
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            # Count Flask routes
            route_count = len(re.findall(r'@app\.route', content))
            
            # Estimate required routes for maternal health system
            required_routes = [
                "login", "register", "dashboard", "patients", "appointments",
                "vitals", "pregnancy", "medical_history", "analytics"
            ]
            
            completeness = min(100.0, (route_count / len(required_routes)) * 100)
            return completeness
            
        except FileNotFoundError:
            return 0.0
    
    def _analyze_input_validation(self) -> float:
        """Analyze input validation coverage"""
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            # Look for validation patterns
            validation_patterns = [
                r'request\.form\.get',
                r'request\.args\.get',
                r'if.*:',
                r'validate',
                r'required'
            ]
            
            validation_score = 0
            for pattern in validation_patterns:
                matches = len(re.findall(pattern, content, re.IGNORECASE))
                validation_score += min(20, matches)  # Cap at 20 per pattern
            
            return min(100.0, validation_score)
            
        except FileNotFoundError:
            return 0.0
    
    def _calculate_defect_density(self) -> float:
        """Calculate defect density (simulated)"""
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            # Look for potential code smells and issues
            defect_patterns = [
                r'print\(',  # Debug prints
                r'TODO|FIXME|XXX',  # Technical debt
                r'except:',  # Bare except clauses
                r'pass\s*$',  # Empty pass statements
            ]
            
            defect_count = 0
            for line in lines:
                for pattern in defect_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        defect_count += 1
            
            # Calculate defects per KLOC
            kloc = len(lines) / 1000
            defect_density = defect_count / kloc if kloc > 0 else 0
            
            return defect_density
            
        except FileNotFoundError:
            return 0.0
    
    def _analyze_error_handling(self) -> float:
        """Analyze error handling coverage"""
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            # Count functions and error handling
            function_count = len(re.findall(r'def\s+\w+', content))
            try_count = len(re.findall(r'try:', content))
            
            if function_count == 0:
                return 0.0
            
            error_handling_percentage = (try_count / function_count) * 100
            return min(100.0, error_handling_percentage)
            
        except FileNotFoundError:
            return 0.0
    
    def _analyze_code_stability(self) -> float:
        """Analyze code stability based on complexity"""
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            # Calculate cyclomatic complexity indicators
            complexity_indicators = [
                r'\bif\b',
                r'\belif\b', 
                r'\bwhile\b',
                r'\bfor\b',
                r'\bexcept\b',
                r'\band\b',
                r'\bor\b'
            ]
            
            complexity_score = 0
            for pattern in complexity_indicators:
                matches = len(re.findall(pattern, content, re.IGNORECASE))
                complexity_score += matches
            
            # Normalize to stability score (inverse relationship)
            stability_score = max(0.0, 100.0 - (complexity_score / 10))
            return min(100.0, stability_score)
            
        except FileNotFoundError:
            return 0.0
    
    def _analyze_ui_consistency(self) -> float:
        """Analyze UI consistency (simulated)"""
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            # Look for template consistency patterns
            template_patterns = [
                r'bootstrap',
                r'navbar',
                r'container',
                r'btn-',
                r'form-'
            ]
            
            consistency_score = 0
            for pattern in template_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    consistency_score += 20
            
            return min(100.0, consistency_score + 20)  # Base score of 20
            
        except FileNotFoundError:
            return 0.0
    
    def _analyze_navigation_complexity(self) -> float:
        """Analyze navigation complexity"""
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            # Count routes and navigation depth
            route_count = len(re.findall(r'@app\.route', content))
            
            # Simulate complexity based on route count
            # More routes = potentially more complex navigation
            complexity = min(10.0, route_count / 2.0)
            return complexity
            
        except FileNotFoundError:
            return 10.0  # High complexity as worst case
    
    def _analyze_form_feedback(self) -> float:
        """Analyze form validation feedback quality"""
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            # Look for feedback mechanisms
            feedback_patterns = [
                r'flash\(',
                r'error',
                r'validation',
                r'required'
            ]
            
            feedback_score = 0
            for pattern in feedback_patterns:
                matches = len(re.findall(pattern, content, re.IGNORECASE))
                feedback_score += min(25, matches)
            
            return min(100.0, feedback_score)
            
        except FileNotFoundError:
            return 0.0
    
    def _analyze_code_efficiency(self) -> float:
        """Analyze code efficiency"""
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            # Look for efficiency indicators
            efficiency_patterns = [
                r'\.filter\(',  # Database filtering
                r'\.limit\(',  # Result limiting
                r'cache',      # Caching mechanisms
                r'index'       # Database indexes
            ]
            
            efficiency_score = 50  # Base score
            for pattern in efficiency_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    efficiency_score += 10
            
            return min(100.0, efficiency_score)
            
        except FileNotFoundError:
            return 0.0
    
    def _analyze_database_efficiency(self) -> float:
        """Analyze database query efficiency"""
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            # Look for database optimization patterns
            optimization_patterns = [
                r'\.join\(',       # Proper joins
                r'\.filter\(',     # Filtering
                r'\.order_by\(',   # Ordering
                r'index'           # Index usage
            ]
            
            optimization_score = 0
            for pattern in optimization_patterns:
                matches = len(re.findall(pattern, content, re.IGNORECASE))
                optimization_score += min(20, matches)
            
            return min(100.0, optimization_score + 30)  # Base score of 30
            
        except FileNotFoundError:
            return 0.0
    
    def _analyze_resource_usage(self) -> float:
        """Analyze resource usage patterns"""
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            # Look for resource-conscious patterns
            resource_patterns = [
                r'with open',      # Context managers
                r'close\(',        # Resource cleanup
                r'finally:',       # Cleanup blocks
                r'del '            # Explicit deletion
            ]
            
            resource_score = 60  # Base score
            for pattern in resource_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    resource_score += 10
            
            return min(100.0, resource_score)
            
        except FileNotFoundError:
            return 0.0
    
    def _analyze_code_structure(self) -> float:
        """Analyze code structure quality"""
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            # Look for good structure patterns
            structure_patterns = [
                r'class\s+\w+',   # Classes
                r'def\s+\w+',     # Functions
                r'"""\s*.*?\s*"""',  # Docstrings
                r'import\s+\w+',  # Imports
            ]
            
            structure_score = 0
            for pattern in structure_patterns:
                matches = len(re.findall(pattern, content, re.IGNORECASE | re.DOTALL))
                structure_score += min(20, matches)
            
            return min(100.0, structure_score)
            
        except FileNotFoundError:
            return 0.0
    
    def _analyze_documentation_quality(self) -> float:
        """Analyze documentation quality"""
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            # Count comment lines and docstrings
            comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
            docstring_lines = sum(1 for line in lines if '"""' in line or "'''" in line)
            total_lines = len(lines)
            
            if total_lines == 0:
                return 0.0
            
            documentation_percentage = ((comment_lines + docstring_lines) / total_lines) * 100
            return min(100.0, documentation_percentage * 5)  # Scale up
            
        except FileNotFoundError:
            return 0.0
    
    def _analyze_modularity(self) -> float:
        """Analyze code modularity"""
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            # Count classes and functions
            class_count = len(re.findall(r'class\s+\w+', content))
            function_count = len(re.findall(r'def\s+\w+', content))
            
            # Calculate modularity score
            # More functions and classes = better modularity
            modularity_score = min(100.0, (class_count * 10) + (function_count * 2))
            return modularity_score
            
        except FileNotFoundError:
            return 0.0
    
    def _analyze_platform_independence(self) -> float:
        """Analyze platform independence"""
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            # Look for platform-specific code
            platform_specific = [
                r'windows',
                r'linux', 
                r'macos',
                r'os\.path',
                r'sys\.platform'
            ]
            
            platform_issues = 0
            for pattern in platform_specific:
                if re.search(pattern, content, re.IGNORECASE):
                    platform_issues += 1
            
            # Lower issues = better platform independence
            independence_score = max(0.0, 100.0 - (platform_issues * 20))
            return independence_score
            
        except FileNotFoundError:
            return 0.0
    
    def _analyze_configuration_management(self) -> float:
        """Analyze configuration management"""
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            # Look for configuration patterns
            config_patterns = [
                r'os\.environ',
                r'config',
                r'SECRET_KEY',
                r'DATABASE_URL'
            ]
            
            config_score = 0
            for pattern in config_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    config_score += 25
            
            return min(100.0, config_score)
            
        except FileNotFoundError:
            return 0.0
    
    def _analyze_dependency_management(self) -> float:
        """Analyze dependency management"""
        try:
            # Check for requirements.txt
            if os.path.exists("requirements.txt"):
                with open("requirements.txt", "r") as f:
                    requirements = f.read()
                
                # Count dependencies
                dependency_count = len([line for line in requirements.split('\n') if line.strip()])
                
                # Score based on reasonable dependency count
                if dependency_count <= 10:
                    return 90.0
                elif dependency_count <= 20:
                    return 75.0
                else:
                    return 60.0
            else:
                return 30.0  # No requirements file
                
        except Exception:
            return 0.0
    
    def run_full_analysis(self) -> Dict:
        """Run complete quality analysis"""
        print("=" * 60)
        print("SOFTWARE QUALITY METRICS ANALYSIS")
        print("ISO 9126 Quality Model Implementation")
        print("=" * 60)
        
        results = {}
        
        # Run all analyses
        results["Functionality"] = self.analyze_functionality()
        results["Reliability"] = self.analyze_reliability()
        results["Usability"] = self.analyze_usability()
        results["Efficiency"] = self.analyze_efficiency()
        results["Maintainability"] = self.analyze_maintainability()
        results["Portability"] = self.analyze_portability()
        
        # Calculate overall scores
        overall_scores = {}
        for char_name, characteristic in self.characteristics.items():
            overall_scores[char_name] = characteristic.calculate_score()
        
        results["overall_scores"] = overall_scores
        results["total_quality_score"] = sum(overall_scores.values()) / len(overall_scores)
        
        return results
    
    def generate_report(self, results: Dict) -> str:
        """Generate comprehensive quality report"""
        report = []
        report.append("\n" + "=" * 80)
        report.append("SOFTWARE QUALITY METRICS REPORT")
        report.append("Chapter 8: Measuring External Software Metrics - Quality")
        report.append(f"Project: Maternova - Maternal Health Management System")
        report.append(f"Analysis Date: {self.analysis_date.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)
        
        report.append("\nEXECUTIVE SUMMARY:")
        report.append(f"Overall Quality Score: {results['total_quality_score']:.1f}/100")
        
        # Quality grade
        score = results['total_quality_score']
        if score >= 90:
            grade = "A (Excellent)"
        elif score >= 80:
            grade = "B (Good)"
        elif score >= 70:
            grade = "C (Average)"
        elif score >= 60:
            grade = "D (Below Average)"
        else:
            grade = "F (Poor)"
        
        report.append(f"Quality Grade: {grade}")
        
        report.append("\nQUALITY CHARACTERISTICS SCORES:")
        report.append("-" * 40)
        
        for char_name, score in results["overall_scores"].items():
            report.append(f"{char_name:15}: {score:6.1f}/100")
        
        report.append("\nDETAILED METRICS:")
        report.append("-" * 40)
        
        for char_name, characteristic in self.characteristics.items():
            report.append(f"\n{char_name.upper()}:")
            report.append(f"  Description: {characteristic.description}")
            report.append(f"  Score: {characteristic.calculate_score():.1f}/100")
            report.append("  Metrics:")
            
            for metric in characteristic.metrics:
                target_str = f" (Target: {metric.target})" if metric.target else ""
                report.append(f"    - {metric.name}: {metric.value:.1f} {metric.unit}{target_str}")
                report.append(f"      {metric.description}")
        
        report.append("\nRECOMMENDATIONS:")
        report.append("-" * 40)
        
        # Generate recommendations based on scores
        for char_name, score in results["overall_scores"].items():
            if score < 70:
                report.append(f"• Improve {char_name}: Score {score:.1f} is below acceptable threshold")
                if char_name == "Functionality":
                    report.append("  - Increase test coverage and API completeness")
                elif char_name == "Reliability":
                    report.append("  - Add more error handling and reduce code complexity")
                elif char_name == "Usability":
                    report.append("  - Improve UI consistency and form feedback")
                elif char_name == "Efficiency":
                    report.append("  - Optimize database queries and resource usage")
                elif char_name == "Maintainability":
                    report.append("  - Improve documentation and code structure")
                elif char_name == "Portability":
                    report.append("  - Externalize configuration and reduce platform dependencies")
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)


def main():
    """Main execution function"""
    print("Starting Software Quality Metrics Analysis...")
    print("This may take a few moments...\n")
    
    # Initialize analyzer
    analyzer = QualityMetricsAnalyzer()
    
    # Run analysis
    results = analyzer.run_full_analysis()
    
    # Generate and display report
    report = analyzer.generate_report(results)
    print(report)
    
    # Save results to JSON
    output_data = {
        "analysis_date": analyzer.analysis_date.isoformat(),
        "total_quality_score": results["total_quality_score"],
        "characteristic_scores": results["overall_scores"],
        "detailed_metrics": {}
    }
    
    for char_name, characteristic in analyzer.characteristics.items():
        output_data["detailed_metrics"][char_name] = {
            "description": characteristic.description,
            "score": characteristic.calculate_score(),
            "metrics": [
                {
                    "name": metric.name,
                    "value": metric.value,
                    "unit": metric.unit,
                    "description": metric.description,
                    "target": metric.target
                }
                for metric in characteristic.metrics
            ]
        }
    
    # Save to file
    with open("quality_metrics_results.json", "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\nResults saved to: quality_metrics_results.json")
    print(f"Overall Quality Score: {results['total_quality_score']:.1f}/100")


if __name__ == "__main__":
    main()

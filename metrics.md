Measuring Internal Product Attributes: Software Size
1. Introduction
Software size is an internal product attribute that describes a software system based on its structure without executing it. It is an important metric used to estimate:
•	Development effort 
•	Cost 
•	Productivity 
In this implementation, software size is measured using length-based metrics, specifically:
•	Lines of Code (LOC) 
•	Halstead Metrics 
2. Objectives
The objectives of this implementation are to:
•	Measure the physical size of the system (app.py) 
•	Analyze the internal structure of the code 
•	Provide quantitative metrics for evaluating software complexity and maintainability 
3. Metrics Implemented
3.1 Lines of Code (LOC)
LOC measures the physical size of the software system.
Metrics Computed:
•	Total LOC → Total number of lines in the file 
•	Blank Lines → Empty lines 
•	Comment Lines (CLOC) → Lines containing comments 
•	Effective LOC (NCLOC) → Executable lines 
•	Comment Density → Ratio of comment lines to total lines 
Formula:
LOC = NCLOC + CLOC
Comment Density:
Comment Density = CLOC / LOC
Implementation:
•	The file is read line by line 
•	Blank lines are identified using:
line.strip() == ""
•	Comment lines are detected by checking for the presence of # in each line 
•	Effective LOC is computed by excluding blank and comment lines 
•	Comment density is calculated as the ratio of comment lines to total lines 
Improvements Made:
•	Inline comments are now detected (e.g., x = 5 # comment) 
•	Comment density was added to provide insight into documentation quality 
Significance:
•	Simple and easy to compute 
•	Correlates with development effort 
•	Comment density helps evaluate code documentation 
Limitations:
•	Depends on coding style 
•	May slightly overestimate comments if # appears inside strings 
•	Does not reflect functionality 
3.2 Halstead Metrics
Halstead metrics measure software size based on operators and operands.
Definitions:
•	μ₁ → Number of distinct operators 
•	μ₂ → Number of distinct operands 
•	N₁ → Total occurrences of operators 
•	N₂ → Total occurrences of operands 
Derived Metrics:
Program Vocabulary (μ):
μ = μ₁ + μ₂
Program Length (N):
N = N₁ + N₂
Implementation:
•	Python’s tokenize module is used for lexical analysis 
•	Operators are identified using token type OP 
•	Operands include: 
o	Variable names 
o	Numbers 
o	Strings 
•	Sets are used to count distinct elements 
•	Counters track total occurrences 
Improvements Made:
•	Error handling was added using try-except to prevent crashes during tokenization 
•	This ensures the analyzer works reliably even if the code contains unexpected formatting 
Significance:
•	Measures code complexity 
•	Reflects mental effort required to write the program 
•	Useful for estimating maintainability 
Limitations:
•	Language dependent 
•	Token classification may vary 
4. Tools Used
•	Python 
•	Built-in modules: 
o	tokenize (for lexical analysis) 
o	re (for pattern matching) 
o	io (for reading code as a stream) 
5. Results
Example output from analyzing app.py:
LOC Metrics:
Total LOC: 2967
Blank Lines: 176
Comment Lines: 191
Effective LOC: 2600
Comment Density: 0.06

Halstead Metrics:
Distinct Operators (μ1): 17
Distinct Operands (μ2): 341
Program Vocabulary (μ): 358
Program Length (N): 3638

6. Discussion
The LOC metric provides a simple and direct measurement of software size, while Halstead metrics provide deeper insight into code complexity.
The addition of comment density enhances the analysis by evaluating the level of code documentation.
Together, these metrics provide a more comprehensive understanding of:
•	Code size 
•	Code complexity 
•	Maintainability 
•	Documentation quality 
7. Conclusion
The implementation successfully demonstrates how internal product attributes can be measured using automated tools. By combining LOC and Halstead metrics, along with improvements such as comment density and error handling, the system provides a reliable and meaningful analysis of software size.
8. Future Improvements
•	Implement Cyclomatic Complexity 
•	Improve comment detection using advanced parsing 
•	Analyze multiple files instead of a single file 
•	Integrate metrics into the Flask dashboard 
•	Visualize results using graphs


import re
import tokenize
from io import BytesIO

class SoftwareSizeAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.code = self._read_file()

    def _read_file(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return f.read()

    #LOC METRICS
    def compute_loc(self):
        lines = self.code.splitlines()

        total_lines = len(lines)
        blank_lines = sum(1 for line in lines if line.strip() == "")

        # Improved comment detection (includes inline comments)
        comment_lines = sum(1 for line in lines if "#" in line)

        # Effective LOC
        ncloc = total_lines - blank_lines - comment_lines

        # Comment density (from PDF concept)
        comment_density = comment_lines / total_lines if total_lines > 0 else 0

        return {
            "Total LOC": total_lines,
            "Blank Lines": blank_lines,
            "Comment Lines (CLOC)": comment_lines,
            "Effective LOC (NCLOC)": ncloc,
            "Comment Density": round(comment_density, 2)
        }

    # HALSTEAD METRICS
    def compute_halstead(self):
        operators = set()
        operands = set()
        operator_count = 0
        operand_count = 0

        try:
            tokens = tokenize.tokenize(BytesIO(self.code.encode('utf-8')).readline)

            for token in tokens:
                token_type = token.type
                token_string = token.string

                if token_type == tokenize.OP:
                    operators.add(token_string)
                    operator_count += 1

                elif token_type == tokenize.NAME:
                    operands.add(token_string)
                    operand_count += 1

                elif token_type in (tokenize.NUMBER, tokenize.STRING):
                    operands.add(token_string)
                    operand_count += 1

        except tokenize.TokenError:
            # Prevent crashing if tokenization fails
            pass

        mu1 = len(operators)
        mu2 = len(operands)
        N1 = operator_count
        N2 = operand_count

        vocabulary = mu1 + mu2
        length = N1 + N2

        return {
            "Distinct Operators (μ1)": mu1,
            "Distinct Operands (μ2)": mu2,
            "Total Operators (N1)": N1,
            "Total Operands (N2)": N2,
            "Program Vocabulary (μ)": vocabulary,
            "Program Length (N)": length
        }

    # RUN ANALYSIS
    def analyze(self):
        return {
            "LOC Metrics": self.compute_loc(),
            "Halstead Metrics": self.compute_halstead()
        }


# EXAMPLE USAGE
if __name__ == "__main__":
    analyzer = SoftwareSizeAnalyzer("app.py")
    results = analyzer.analyze()

    print("\n=== SOFTWARE SIZE ANALYSIS ===\n")

    print(">> LOC METRICS")
    for k, v in results["LOC Metrics"].items():
        print(f"{k}: {v}")

    print("\n>> HALSTEAD METRICS")
    for k, v in results["Halstead Metrics"].items():
        print(f"{k}: {v}")
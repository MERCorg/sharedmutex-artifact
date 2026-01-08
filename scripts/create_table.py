import argparse
import json
import re

from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple


def sanitize_str(s: str) -> str:
    """Sanitize a string such that it can be rendered by pdflatex"""
    return s.replace("_", r"\_")


def benchmark_to_latex(path: str) -> None:
    """Convert benchmark JSON data to LaTeX tables"""
    # Read the json file
    path_obj = Path(path)
    output = path_obj.read_text()

    # The regex to extract the benchmark ID
    name_re = re.compile(r"(.*) ([0-9]*) ([0-9]*) ([0-9]*)")

    # nested dictionary: name -> read_ratio -> list of (num_threads, estimate)
    benchmarks: Dict[str, Dict[int, List[Tuple[int, float]]]] = defaultdict(
        lambda: defaultdict(list)
    )

    # Take the benchmark data into memory
    for line in output.splitlines():
        try:
            result = json.loads(line)

            if result.get("reason") == "benchmark-complete":
                # Figure out the benchmark ID
                match = name_re.match(result["id"])
                if match:
                    name = match.group(1)
                    num_threads = int(match.group(2))
                    num_iterations = match.group(3)
                    read_ratio = int(match.group(4))

                    # This is in nanoseconds, convert to milliseconds
                    estimate = result["mean"]["estimate"] / 1_000_000.0

                    print(
                        f"{name} {num_threads} {num_iterations} {read_ratio} took {estimate}"
                    )

                    # Insert the entry into the correct hashtable
                    benchmarks[name][read_ratio].append((num_threads, estimate))
        except (json.JSONDecodeError, KeyError):
            continue

    # Construct a table from the data
    latex_output = path_obj.with_suffix(".tex")

    with open(latex_output, "w") as file:
        file.write(r"""\documentclass{article}

\usepackage{tikz}
\usepackage{pgfplots}

\pgfplotsset{compat=1.18}

\begin{document}
""")

        # Figure out the tables from the read_ratio
        read_ratios = set()
        for result in benchmarks.values():
            read_ratios.update(result.keys())

        threads = set()
        for result in benchmarks.values():
            for timing in result.values():
                for num_threads, _ in timing:
                    threads.add(num_threads)

        # Sort the tables
        read_ratios = sorted(read_ratios)
        threads = sorted(threads)

        print(f"Read ratios: [{', '.join(map(str, read_ratios))}]")
        print(f"Threads: [{', '.join(map(str, threads))}]")

        # Construct one table per ratio
        for ratio in read_ratios:
            file.write(r"""\begin{table}[h]
\begin{tabular}{r|r|r|r|r|r|r}
name & 1 & 2 & 4 & 8 & 16 & 20 \\ \hline
""")

            for name, result in benchmarks.items():
                file.write(sanitize_str(name))

                if ratio in result:
                    timing = result[ratio]
                    for _, time in timing:
                        file.write(f" & {time:.2f}")

                file.write(r" \\" + "\n")

            # Derive the read percentage
            read_percentage = 1.0 - 1.0 / ratio

            file.write(f"""\end{{tabular}}
\caption{{Timing benchmarks for number of threads in ms, with read percentage {read_percentage}.}}
\end{{table}}

""")

        file.write(r"\end{document}" + "\n")

def main():
    parser = argparse.ArgumentParser(description="Convert benchmark JSON to LaTeX tables")
    parser.add_argument("input_file", type=str, help="Path to the benchmark JSON file.")
    args = parser.parse_args()

    benchmark_to_latex(args.input_file)


if __name__ == "__main__":
    main()

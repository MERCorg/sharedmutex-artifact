import argparse
import subprocess
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    parser = argparse.ArgumentParser(description="Script to run the benchmarks")
    parser.add_argument("output_dir", type=str, help="The output directory.")
    args = parser.parse_args()
    output_file = os.path.join(args.output_dir, "benchmarks.json")
    os.makedirs(args.output_dir, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        subprocess.run(
            ["cargo", "criterion", "--message-format=json"],
            check=True,
            cwd=os.path.join(SCRIPT_DIR, "../benchmarks"),
            stdout=f,
        )


if __name__ == "__main__":
    main()

import subprocess
import json
import os
import traceback


def run_gitleaks_scan(path):
    try:
        output_dir = "results"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "gitleaks.json")

        subprocess.run([
            "gitleaks", "detect",
            "--source", path,
            "--report-format", "json",
            "--report-path", output_file
        ], check=True)

        with open(output_file) as f:
            return json.load(f)

    except subprocess.CalledProcessError as e:
        return {"error": "Gitleaks scan failed", "details": str(e)}
    except Exception as e:
        return {"error": "Exception in Gitleaks", "details": traceback.format_exc()}

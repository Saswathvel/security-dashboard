import subprocess
import json
import os
import traceback


def run_codeql_scan(path, language="javascript"):
    try:
        db_path = os.path.join(path, "codeql-db")
        output_dir = os.path.join(path, "results")
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "codeql.sarif")

        # Step 1: Create database
        subprocess.run([
            "codeql", "database", "create", db_path,
            "--language=" + language,
            "--source-root", path,
            "--overwrite"
        ], check=True)

        # Step 2: Run analysis
        subprocess.run([
            "codeql", "database", "analyze", db_path,
            f"codeql/{language}-queries",
            "--format=sarifv2.1.0",
            "--output", output_file
        ], check=True)

        # Step 3: Load results
        with open(output_file) as f:
            return json.load(f)

    except subprocess.CalledProcessError as e:
        return {"error": "CodeQL scan failed", "details": str(e)}
    except Exception as e:
        return {"error": "Exception in CodeQL", "details": traceback.format_exc()}

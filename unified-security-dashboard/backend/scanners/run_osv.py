import os
import subprocess

def run_osv_scan(repo_dir):
    print("📊 Running OSV-Scalibr...")
    output_file = os.path.join("results", "osv.textproto")
    os.makedirs("results", exist_ok=True)

    try:
        result = subprocess.run(
            [
                "scalibr",
                "--root", repo_dir,
                "--o", output_file
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return [{
                "tool": "OSV-Scalibr",
                "error": "OSV-Scalibr failed",
                "details": result.stderr
            }]

        # Instead of trying JSON, just read raw textproto
        with open(output_file, "r") as f:
            raw_text = f.read()

        return [{
            "tool": "OSV-Scalibr",
            "raw_output": raw_text[:500] + ("..." if len(raw_text) > 500 else "")
        }]

    except Exception as e:
        return [{
            "tool": "OSV-Scalibr",
            "error": "Unexpected error",
            "details": str(e)
        }]

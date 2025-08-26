import os
import subprocess
import tempfile
import shutil
import traceback

from scanners.run_codeql import run_codeql_scan
from scanners.run_gitleaks import run_gitleaks_scan
from scanners.run_syft import generate_sbom
from scanners.run_osv import run_osv_scan
from scanners.parse_results import parse_codeql, parse_syft, parse_osv, parse_gitleaks


def scan_project(input_type, repo_url_or_path):
    temp_dir = tempfile.mkdtemp()
    output_dir = tempfile.mkdtemp()

    try:
        if input_type != "git":
            return {"error": "Only Git input is supported."}, 400

        # Clone repo
        repo_dir = os.path.join(temp_dir, "repo")
        os.makedirs(repo_dir, exist_ok=True)
        print(f"📥 Cloning {repo_url_or_path} ...")
        subprocess.run(["git", "clone", repo_url_or_path, repo_dir], check=True)

        # Install deps if Node.js project
        package_json = os.path.join(repo_dir, "package.json")
        if os.path.exists(package_json):
            print("📦 Running npm install...")
            subprocess.run(["npm", "install"], cwd=repo_dir, check=True)
        else:
            print("⚠️ No package.json found. Skipping npm install.")

        # Run scanners
        print("🔐 Running Gitleaks...")
        gitleaks_results = run_gitleaks_scan(repo_dir)

        print("📦 Generating SBOM with Syft...")
        sbom_file = generate_sbom(repo_dir)

        print("📊 Running OSV-Scalibr...")
        osv_results = run_osv_scan(repo_dir)   # ✅ FIX: use repo_dir instead of sbom_results

        print("🧠 Running CodeQL...")
        codeql_results = run_codeql_scan(repo_dir)

        # Parse results
        print("✅ Parsing results...")
        final_results = {
            "codeql": parse_codeql(codeql_results),
            "syft": parse_syft(sbom_file),      # ✅ pass sbom.json path
            "osv": parse_osv(osv_results),
            "gitleaks": parse_gitleaks(gitleaks_results),
        }

        return final_results

    except subprocess.CalledProcessError as e:
        print(f"❌ Subprocess error: {e}")
        return {"error": str(e), "details": traceback.format_exc()}, 500

    except Exception as ex:
        print(f"🔥 Unexpected error: {ex}")
        return {"error": str(ex), "details": traceback.format_exc()}, 500

    finally:
        print("🧹 Cleaning up...")
        shutil.rmtree(temp_dir, ignore_errors=True)
        shutil.rmtree(output_dir, ignore_errors=True)

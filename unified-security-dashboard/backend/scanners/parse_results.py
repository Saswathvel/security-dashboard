import json
import re


def parse_codeql(codeql_result):
    results = []
    try:
        if not codeql_result or "error" in codeql_result:
            return [{"tool": "CodeQL", "error": codeql_result.get("error", "No results"),
                     "details": codeql_result.get("details", "")}]

        for run in codeql_result.get("runs", []):
            for result in run.get("results", []):
                rule = result.get("ruleId", "N/A")
                message = result.get("message", {}).get("text", "")
                file_path = (
                    result.get("locations", [{}])[0]
                    .get("physicalLocation", {})
                    .get("artifactLocation", {})
                    .get("uri", "")
                )

                results.append({
                    "tool": "CodeQL",
                    "rule": rule,
                    "message": message,
                    "file": file_path
                })
    except Exception as e:
        results.append({"tool": "CodeQL", "error": f"Parse error: {e}"})
    return results


def parse_syft(sbom_path):
    results = []
    try:
        # Load SBOM JSON from file
        with open(sbom_path, "r") as f:
            sbom_result = json.load(f)

        for artifact in sbom_result.get("artifacts", []):
            name = artifact.get("name", "")
            version = artifact.get("version", "")
            type_ = artifact.get("type", "")
            results.append({
                "tool": "Syft",
                "name": name,
                "version": version,
                "type": type_
            })

    except Exception as e:
        results.append({"tool": "Syft", "error": f"Parse error: {e}"})

    return results


def parse_osv(osv_result):
    results = []
    try:
        if isinstance(osv_result, list):
            for item in osv_result:
                raw_text = item.get("raw_output", "")

                # Try extracting CVEs
                cves = re.findall(r"CVE-\d{4}-\d+", raw_text)

                if cves:
                    for cve in cves:
                        results.append({
                            "tool": "OSV-Scalibr",
                            "id": cve,
                            "severity": "UNKNOWN",
                            "details": "Found by OSV-Scalibr"
                        })
                else:
                    # Fallback: show a friendly status
                    results.append({
                        "tool": "OSV-Scalibr",
                        "status": "No CVEs detected",
                        "summary": "Scan completed successfully but no vulnerabilities found."
                    })
        else:
            results.append({
                "tool": "OSV-Scalibr",
                "error": "Unexpected result format"
            })

    except Exception as e:
        results.append({"tool": "OSV-Scalibr", "error": f"Parse error: {e}"})

    return results




def parse_gitleaks(gitleaks_result):
    results = []
    try:
        if not gitleaks_result or "error" in gitleaks_result:
            return [{"tool": "Gitleaks", "error": gitleaks_result.get("error", "No results"),
                     "details": gitleaks_result.get("details", "")}]

        for leak in gitleaks_result:
            results.append({
                "tool": "Gitleaks",
                "rule": leak.get("rule", ""),
                "file": leak.get("file", ""),
                "secret": leak.get("secret", "[REDACTED]"),
                "line": leak.get("line", "")
            })
    except Exception as e:
        results.append({"tool": "Gitleaks", "error": f"Parse error: {e}"})
    return results

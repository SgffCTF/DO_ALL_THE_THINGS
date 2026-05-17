import subprocess
from pathlib import Path
import json
import html

def run(cmd, cwd=None):
    print(f"[+] Running: {' '.join(cmd)} (cwd={cwd})")
    subprocess.run(cmd, cwd=cwd, check=True)


def sarif_to_html(sarif_path: Path, html_path: Path):
    data = json.loads(sarif_path.read_text())

    runs = data.get("runs", [])
    results = runs[0].get("results", []) if runs else []

    rows = ""

    for r in results:
        rule = r.get("ruleId", "unknown")
        message = r.get("message", {}).get("text", "")
        level = r.get("level", "note")

        loc = r.get("locations", [{}])[0]
        phys = loc.get("physicalLocation", {})
        artifact = phys.get("artifactLocation", {})
        region = phys.get("region", {})

        file = artifact.get("uri", "unknown")
        line = region.get("startLine", "?")

        snippet = region.get("snippet", {}).get("text", "")

        if snippet:
            snippet = html.escape(snippet)
            snippet_html = f"""
            <pre style="
                background:#0f172a;
                color:#e2e8f0;
                padding:10px;
                border-radius:6px;
                overflow-x:auto;
                font-size:12px;
            ">{snippet}</pre>
            """
        else:
            snippet_html = "<i style='color:gray'>no snippet</i>"

        # severity color
        color = {
            "error": "#ff4d4f",
            "warning": "#faad14",
            "note": "#1677ff"
        }.get(level, "#999")

        rows += f"""
        <tr>
            <td style="color:{color}; font-weight:bold;">{level}</td>
            <td>{rule}</td>
            <td>{file}</td>
            <td>{line}</td>
            <td>{snippet_html}</td>
            <td>{html.escape(message)}</td>
        </tr>
        """

    html_report = f"""
    <html>
    <head>
        <title>Security Report</title>
        <style>
            body {{
                font-family: Arial;
                background: #0b1220;
                color: #e5e7eb;
            }}

            table {{
                border-collapse: collapse;
                width: 100%;
            }}

            td, th {{
                border: 1px solid #1f2937;
                padding: 8px;
                vertical-align: top;
            }}

            th {{
                background: #111827;
                color: white;
            }}

            tr:nth-child(even) {{
                background: #0f172a;
            }}
        </style>
    </head>
    <body>
        <h1>Findings: {len(results)}</h1>
        <table>
            <tr>
                <th>Severity</th>
                <th>Rule</th>
                <th>File</th>
                <th>Line</th>
                <th>Snippet</th>
                <th>Message</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """

    html_path.write_text(html_report)
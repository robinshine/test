import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def escape_message(value):
    return value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def changed_ranges(path):
    if os.environ.get("GITHUB_EVENT_NAME") != "pull_request":
        return []

    # The default pull request checkout is a merge commit with the base as its first parent.
    diff = subprocess.check_output(
        [
            "git", "--literal-pathspecs", "diff", "--no-color", "--no-ext-diff",
            "--no-textconv", "--unified=0", "HEAD^1", "HEAD", "--", path,
        ],
        encoding="utf-8",
        errors="replace",
    )
    ranges = []
    for hunk in re.finditer(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", diff, re.MULTILINE):
        start = int(hunk[1])
        ranges.append(range(start, start + int(hunk[2] or "1")))
    return ranges


def annotate(report_path):
    workspace = Path.cwd().resolve()
    levels = {"error": "error", "warning": "warning", "info": "notice"}
    changed_annotations = []
    other_annotations = []

    for file in ET.parse(report_path).getroot().findall("file"):
        source = Path(file.attrib["name"]).resolve()
        findings = file.findall("error")
        if not findings or not source.is_relative_to(workspace):
            continue

        path = source.relative_to(workspace).as_posix()
        ranges = changed_ranges(path)
        escaped_path = escape_message(path).replace(":", "%3A").replace(",", "%2C")
        for finding in findings:
            level = levels.get(finding.get("severity"))
            if level is None:
                continue

            line = max(1, int(finding.get("line", "1")))
            column = int(finding.get("column", "0"))
            location = f"file={escaped_path},line={line}"
            if column > 0:
                location += f",col={column}"

            message = escape_message(finding.attrib["message"])
            annotation = f"::{level} {location},title=Checkstyle::{message}"
            if any(line in changed for changed in ranges):
                changed_annotations.append(annotation)
            else:
                other_annotations.append(annotation)

    # GitHub caps annotations per step, so emit findings on changed lines first.
    for annotation in changed_annotations + other_annotations:
        print(annotation)


if __name__ == "__main__":
    annotate(sys.argv[1])

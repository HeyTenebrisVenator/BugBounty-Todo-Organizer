# ReconBoard

A lightweight reconnaissance and bug bounty task management application built with Python and Tkinter.

ReconBoard helps security researchers organize reconnaissance activities, track target progress, maintain investigation notes, and manage custom workflows throughout the assessment process.

Instead of using spreadsheets, text files, or scattered notes, ReconBoard provides a centralized dashboard for managing bug bounty and penetration testing engagements.

---

# Overview

ReconBoard was created to solve a common problem faced by bug bounty hunters and penetration testers:

> "How do I keep track of everything I've already tested?"

When working with dozens or hundreds of targets, it is easy to lose track of:

* Reconnaissance tasks already completed
* Interesting findings
* Login pages
* Upload functionality
* Administrative panels
* API endpoints
* Fuzzing activities
* Service enumeration progress

ReconBoard provides a simple way to organize this information per target.

---

# Features

### Target Management

* Add new targets
* Remove targets
* Search targets
* Track progress individually
* Automatically save data

### Reconnaissance Checklist

Each target starts with a predefined checklist including:

* Real IP discovery
* WAF/CDN detection
* Port enumeration
* Service enumeration
* Web application discovery
* Exploit research
* Nuclei scanning
* ZAP scanning
* Login page identification
* Registration flow review
* Password recovery analysis
* Upload functionality discovery
* Internal panel discovery
* Admin area enumeration
* API endpoint discovery

### Progress Tracking

Track completion percentage for each target.

Example:

```text id="8r5wvy"
example.com [74%]
api.example.com [32%]
admin.example.com [100%]
```

### Task Management

* Add custom tasks
* Edit existing tasks
* Delete tasks
* Mark tasks as completed
* Assign priorities

Supported priorities:

* Low
* Medium
* High

### Notes System

Store investigation notes directly inside the target profile.

Example:

```text id="hxpwq5"
Found hidden admin panel:
/internal/admin

Authentication required.

Potential attack surface:
- Password reset flow
- File upload endpoint
```

### Automatic Persistence

All data is automatically stored in a local JSON database.

No external database is required.

---

# Why ReconBoard?

Most bug bounty hunters use:

* Notepad
* Obsidian
* Excel spreadsheets
* Google Sheets
* Markdown files

While these tools work well, they do not provide:

* Progress tracking
* Structured recon workflows
* Task prioritization
* Target-specific organization

ReconBoard was designed specifically for offensive security workflows.

---

# Installation

Clone the repository:

```bash id="3x67w0"
git clone https://github.com/yourusername/reconboard.git
cd reconboard
```

Install dependencies:

```bash id="h5h2ya"
pip install -r requirements.txt
```

Required packages:

```bash id="8zjgg4"
pip install tk
```

---

# Running ReconBoard

Start the application:

```bash id="ag4x7h"
python reconboard.py
```

---

# Interface Overview

### Left Panel

Target management:

* Search targets
* Add targets
* Remove targets
* Reset target tasks

### Main Panel

Target information:

* Progress bar
* Recon checklist
* Custom tasks
* Priority labels

### Notes Section

Store findings, URLs, credentials, attack paths, or any relevant information related to the selected target.

---

# Example Workflow

## Step 1

Add a target:

```text id="jlh69s"
example.com
```

---

## Step 2

Start reconnaissance:

```text id="rjv4ca"
✓ Identify Real IP
✓ Enumerate Ports
✓ Enumerate Services
✓ Run Nuclei
```

Progress:

```text id="yxg0np"
34%
```

---

## Step 3

Add custom tasks:

```text id="9qzcaf"
Investigate GraphQL endpoint
Review JWT implementation
Analyze password reset flow
Check API rate limits
```

---

## Step 4

Store findings:

```text id="uyr6ph"
Potential IDOR found on:

/api/v1/users/{id}

Needs further validation.
```

---

## Step 5

Continue later without losing progress.

ReconBoard automatically saves everything.

---

# Data Storage

All information is stored in:

```text id="4ktmj4"
bug_bounty_tasks.json
```

Example structure:

```json id="vbrihd"
{
  "example.com": {
    "created_at": "2026-05-29T10:00:00",
    "updated_at": "2026-05-29T10:30:00",
    "notes": "Interesting upload functionality found.",
    "tasks": [
      {
        "title": "Run Nuclei",
        "done": true,
        "priority": "High"
      }
    ]
  }
}
```

---

# Use Cases

ReconBoard can be used for:

### Bug Bounty

Track reconnaissance activities across multiple programs.

### Penetration Testing

Organize testing methodology and progress.

### Attack Surface Management

Maintain visibility over discovered assets.

### Red Team Operations

Track assessment progress across environments.

### Security Training

Learn and follow structured reconnaissance methodologies.

---

# Future Roadmap

Planned features include:

* Tags and categories
* Screenshots per target
* Export to Markdown
* Export to HTML reports
* Export to PDF reports
* Severity tracking
* Finding management
* Integration with Nuclei
* Integration with Amass
* Integration with Subfinder
* Integration with Shodan
* Automatic recon templates
* Multi-project support
* Dark mode
* Dashboard statistics
* Risk scoring
* Vulnerability tracking

---

# Example Recon Methodology

```text id="4v6r0f"
Target Discovery
        │
        ▼
ReconBoard
        │
        ▼
Port Enumeration
        │
        ▼
Service Enumeration
        │
        ▼
Web Discovery
        │
        ▼
Vulnerability Discovery
        │
        ▼
Reporting
```

---

# Author

Arthur Witt

Built for bug bounty hunting, penetration testing, attack surface management, and offensive security research.

---

# License

This project is intended for educational purposes, authorized security testing, and research activities only.

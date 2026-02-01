# Kimi Code CLI Cheatsheet for Client Management

Quick commands to manage multiple ISO 42001 clients efficiently.

---

## Daily Operations

### Check All Client Statuses
```
ReadFile: path="client-management/MASTER_TRACKING.md"
```

### Get Specific Client Status
```
ReadFile: path="client-management/clients/[client-name]/99-STATUS.md"
```

### Update Client Progress
```
StrReplaceFile: 
  path="client-management/clients/[client-name]/99-STATUS.md"
  edit={old: "Overall Progress | 50%", new: "Overall Progress | 65%"}
```

---

## Adding New Clients

### Create New Client Folder
```
Shell: command="cp -r client-management/clients/CLIENT-TEMPLATE client-management/clients/[new-client-name]"
```

### Set Up Client Info
```
StrReplaceFile:
  path="client-management/clients/[new-client-name]/00-CLIENT-INFO.md"
  edit=[
    {old: "[COMPANY NAME]", new: "Acme Corp"},
    {old: "[Industry]", new: "Defense"},
    {old: "[Service Tier]", new: "Strategic Roadmap"}
  ]
```

### Add to Master Tracking
```
StrReplaceFile:
  path="client-management/MASTER_TRACKING.md"
  edit={old: "| _Example Client_ |", new: "| Acme Corp | Defense | Implementation | Jan 15 | Mar 30 | 65% | 🟢 On Track | Risk register |\n| _Example Client_ |"}
```

---

## Weekly Review Workflow

### 1. Review All Status Files
```
Shell: command="cat client-management/clients/*/99-STATUS.md"
```

### 2. Find At-Risk Clients
```
Grep: 
  pattern="🟡|🔴"
  path="client-management/MASTER_TRACKING.md"
  output_mode="content"
  -n: true
```

### 3. Check for Missing Evidence
```
Grep:
  pattern="Missing|Pending|⬜"
  path="client-management/clients/*/evidence"
  output_mode="content"
```

### 4. Update Master Dashboard
```
StrReplaceFile:
  path="client-management/MASTER_TRACKING.md"
  edit={old: "Acme Corp | Defense | Implementation | Jan 15 | Mar 30 | 65%", new: "Acme Corp | Defense | Implementation | Jan 15 | Mar 30 | 75%"}
```

---

## Document Generation

### Create Weekly Status for Client
```
Task:
  description="Generate weekly status report"
  prompt="Create a weekly status update for [CLIENT NAME] based on their current progress in ISO 42001 implementation. Use template at client-management/templates/weekly-status-template.md. Current status: [DETAILS]."
  subagent_name="coder"
```

### Generate Gap Analysis
```
Task:
  description="Create client gap analysis"
  prompt="Using client-management/templates/gap-analysis-template.md, create a gap analysis for [CLIENT]. Their current state: [DESCRIPTION]. Target certification: [DATE]."
  subagent_name="coder"
```

---

## Audit Preparation

### Check Audit Readiness
```
ReadFile: path="client-management/clients/[client]/templates/audit-readiness-checklist.md"
```

### Verify All Evidence Present
```
Shell: command="ls -la client-management/clients/[client]/evidence/"
```

### List All Client Policies
```
Glob: pattern="client-management/clients/*/policies/*.md"
```

---

## Reporting

### Generate Weekly Summary
```
Task:
  description="Generate weekly client summary"
  prompt="Review client-management/MASTER_TRACKING.md and all client-management/clients/*/99-STATUS.md files. Generate a weekly summary report using client-management/reports/weekly-summary-template.md format."
  subagent_name="coder"
```

### Count Clients by Stage
```
Shell: command="grep -c 'Discovery' client-management/MASTER_TRACKING.md && grep -c 'Implementation' client-management/MASTER_TRACKING.md && grep -c 'Audit Prep' client-management/MASTER_TRACKING.md"
```

---

## Quick Reference

| Task | Command |
|------|---------|
| View master dashboard | `ReadFile: path="client-management/MASTER_TRACKING.md"` |
| View client status | `ReadFile: path="client-management/clients/[name]/99-STATUS.md"` |
| Update status | `StrReplaceFile` on 99-STATUS.md |
| New client | `cp -r CLIENT-TEMPLATE [new-name]` |
| Find at-risk | `Grep: pattern="🟡\|🔴"` |
| List all clients | `Shell: ls client-management/clients/` |

---

## Tips

1. **Use consistent naming** - lowercase, hyphens for spaces
2. **Update MASTER_TRACKING.md weekly** - Even if no changes, confirm status
3. **Document blockers immediately** - Don't let issues linger
4. **Archive completed clients** - Move to `clients/archived/` when certified

---

*Keep this handy for quick reference*

# 🔄 How to Resume Work on This Project

Quick guide for continuing development on the ISO 42001 certification package.

---

## Quick Resume (30 seconds)

```bash
# 1. Check what we were doing
cd ~/Desktop/iso-42001-certification
git status
git log --oneline -3

# 2. View current state
cat ~/.kimi-agent/STATE.md

# 3. Start Kimi with context
kimi-agent-init
```

---

## Full Resume Routine

### In Your Terminal:

```bash
# Check pickup summary
kimi-pickup

# Start Kimi with full context
kimi-agent-init
```

### In Kimi Code CLI:

```
# Load agent context
ReadFile: path="/Users/brannonsolomon/.kimi-agent/SOUL.md"
ReadFile: path="/Users/brannonsolomon/.kimi-agent/USER.md"
ReadFile: path="/Users/brannonsolomon/.kimi-agent/STATE.md"

# Load today's memory
ReadFile: path="/Users/brannonsolomon/.kimi-agent/memory/2026-01-31.md"

# Or just say:
"Pick up where we left off. Read my STATE.md and tell me what's next."
```

---

## What's In This Repo

| Directory | Purpose | Status |
|-----------|---------|--------|
| `docs/` | Core ISO 42001 documentation | ✅ Complete |
| `templates/` | Reusable templates | ✅ Complete |
| `marketing/` | Sales & marketing materials | ✅ Complete |
| `client-management/` | Multi-client tracking system | ✅ Complete |
| `cmmc-training/` | CMMC + ISO unified offering | ✅ Complete |

---

## Common Tasks

### Add New Client
```bash
cp -r client-management/clients/CLIENT-TEMPLATE \
      client-management/clients/[client-name]
```

### Update GitHub
```bash
git add -A
git commit -m "Description"
git push
```

### Check Client Status
```
ReadFile: path="client-management/MASTER_TRACKING.md"
```

---

## Need Help?

- **Quick commands:** `kimi-help`
- **Agent status:** `kimi-status`
- **Full pickup guide:** `cat ~/.kimi-agent/PICKUP.md`

---

*This project uses the Kimi Agent system for persistent context*

# AIMS Operations Manual

**Internal Use Only - 12th House AI**

Document Control:
- Version: 1.0
- Effective: February 1, 2026
- Owner: Brannon Solomon
- Classification: Internal

---

## Quick Reference

| Document | Purpose | Location |
|----------|---------|----------|
| AI Governance Statement | External-facing principles | `docs/ai-governance-statement.md` |
| AIMS Policy | Full policy for auditors | `docs/12th-house-ai-policy.md` |
| AI Risk Register | Risk tracking | `evidence/ai-risk-register.xlsx` |
| Metrics Tracking | Performance data | `evidence/metrics-tracking.xlsx` |
| Incident Monitoring Plan | Detection systems | `docs/incident-monitoring-plan.md` |
| Internal Audit Checklist | Audit procedures | `templates/internal-audit-checklist.md` |

---

## Quarterly Governance Review Process

**When:** First week of January, April, July, October

**Duration:** 4-6 hours, typically completed over 2 days

### Day 1: Data Collection (2-3 hours)
1. Update Risk Register (`evidence/ai-risk-register.xlsx`)
   - Review all Active risks
   - Close resolved risks
   - Add new risks identified
   - Update review dates

2. Update Metrics Tracking (`evidence/metrics-tracking.xlsx`)
   - Collect uptime data from Vapi/ElevenLabs dashboards
   - Calculate MTTD/MTTR from incident log
   - Document client NPS scores
   - Update bias test results

3. Review Incidents
   - Check incident log for quarter
   - Verify all incidents closed properly
   - Document lessons learned

### Day 2: Analysis & Planning (2-3 hours)
4. Conduct Internal Audit
   - Use `templates/internal-audit-checklist.md`
   - Document findings
   - Assign corrective actions

5. Management Review
   - Review AI objectives progress
   - Assess resource needs
   - Decide on policy updates
   - Plan next quarter priorities

6. Documentation
   - Save review minutes to `evidence/governance-reviews/`
   - Update any policy changes
   - Set calendar reminders for next review

---

## Monthly Operational Tasks

| Week | Task | Time | Tool/Location |
|------|------|------|---------------|
| Week 1 | Review Vapi/ElevenLabs uptime reports | 15 min | Vendor dashboards |
| Week 2 | Spot-check RMF Navigator accuracy (10 samples) | 30 min | Application + reference sources |
| Week 2 | Review AWS CloudTrail for access anomalies | 20 min | AWS Console |
| Week 3 | Check incident log status | 15 min | Incident tracking sheet |
| Week 4 | Update metrics spreadsheet | 30 min | `evidence/metrics-tracking.xlsx` |

---

## Incident Response Quick Guide

### Detection Sources
- **Vapi Dashboard:** Uptime, error rates, latency
- **ElevenLabs Console:** Usage, API errors
- **AWS CloudWatch:** Infrastructure alerts
- **Better Uptime:** External monitoring
- **Client Reports:** Direct email/phone

### Response Times
| Severity | Detect → Notify | Notify → Contain | Total Target |
|----------|-----------------|------------------|--------------|
| Critical | 5 minutes | 30 minutes | 1 hour |
| High | 15 minutes | 2 hours | 4 hours |
| Medium | 1 hour | 24 hours | 48 hours |
| Low | 24 hours | 72 hours | 1 week |

### Escalation
1. **Technical Lead** (Brannon) - First response for all incidents
2. **Risk Owner** (Brannon) - Takes over High/Critical incidents
3. **CEO** (Brannon) - Informed of Critical within 1 hour, leads response

---

## Risk Register Maintenance

### Adding a New Risk
1. Open `evidence/ai-risk-register.xlsx`
2. Add new row with next Risk ID (R00X)
3. Complete all fields:
   - Description (clear, specific)
   - Category (Bias, Privacy, Performance, Compliance, Operational)
   - Affected System (VoiceGuard, RMF Navigator, VISTA, General)
   - Likelihood (1-5)
   - Impact (1-5)
   - Risk Score (auto-calculated: L x I)
   - Risk Level (auto-calculated)
   - Treatment (Avoid, Reduce, Share, Accept)
   - Mitigation Plan (specific actions)
   - Owner (Brannon Solomon)
   - Status (Active, Monitoring, Closed)
   - Review Date (quarterly)
4. Save and commit to git

### Reviewing Risks
- **Active:** Review monthly
- **Monitoring:** Review quarterly
- **Closed:** Retain for 1 year, then archive

---

## Metrics Collection Procedures

### Compliance Metrics
**AI Systems Compliant:**
- Quarterly checklist: `templates/internal-audit-checklist.md`
- Verify each AI system meets all ISO 42001 requirements
- Document any gaps as risks

**Audit Findings:**
- Log from internal audit
- Track status (Open/Closed)
- Assign corrective actions

**Regulatory Violations:**
- Ongoing monitoring of OMB/NIST updates
- Document any inquiries or findings

### Operational Metrics
**AI System Uptime:**
- Vapi Dashboard: Export monthly report
- ElevenLabs Console: Screenshot SLA status
- Calculate: (Total minutes - Downtime) / Total minutes

**MTTD (Mean Time to Detection):**
- From incident log: Alert timestamp - Detection timestamp
- Track per incident, average monthly

**MTTR (Mean Time to Resolution):**
- From incident log: Resolution timestamp - Detection timestamp
- Track by severity level

### Quality Metrics
**Client NPS:**
- Send SurveyMonkey survey within 1 week of engagement completion
- Track responses in metrics spreadsheet
- Follow up with detractors (0-6 score)

**AI Project Success Rate:**
- Define success criteria at project start
- Review at project retrospective
- Calculate: Successful projects / Total projects

**Bias Test Pass Rate:**
- Run quarterly fairness tests
- Use synthetic test datasets
- Document results in metrics spreadsheet

---

## Tool Access Reference

| Tool | Purpose | URL | Login |
|------|---------|-----|-------|
| Vapi Dashboard | Voice AI monitoring | dashboard.vapi.ai | Google OAuth |
| ElevenLabs | Voice synthesis | elevenlabs.io | Email/Password |
| AWS Console | Infrastructure | aws.amazon.com | IAM credentials |
| Better Uptime | External monitoring | betteruptime.com | Email/Password |
| Anthropic Console | Claude API usage | console.anthropic.com | Google OAuth |
| SurveyMonkey | Client surveys | surveymonkey.com | Email/Password |
| GitHub | Documentation | github.com | OAuth |

---

## Document Version Control

All AIMS documents follow this versioning:
- **Major (X.0):** Significant policy changes, annual reviews
- **Minor (x.X):** Operational updates, new tools, clarifications
- **No version:** Evidence files (Risk Register, Metrics) - use date in filename for archives

**Commit messages:**
```
AIMS: Update Risk Register - added R009 (VISTA model drift)
AIMS: Q1 2026 Governance Review completed
AIMS: Revise Section 6.3 - added Risk Register reference
```

---

## Contact & Support

For questions about AIMS operations:
- **Document Owner:** Brannon Solomon
- **Backup:** [Designate when team grows]

---

*Last updated: February 1, 2026*

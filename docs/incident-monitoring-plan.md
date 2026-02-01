# Incident Monitoring Plan

**Document ID:** IMP-001  
**Version:** 1.0  
**Effective Date:** January 2026  
**Owner:** AI Safety Officer  
**Review Cycle:** Quarterly  

---

## 1. Overview

This Incident Monitoring Plan defines the systems, thresholds, and procedures for detecting AI-related incidents across 12th House AI's AI systems portfolio. It operationalizes the requirements defined in Section 11.2 of the AIMS Policy by specifying:

- **What** we monitor (technical metrics, behavioral indicators, external signals)
- **How** we detect incidents (automated alerts, manual reviews, user feedback)
- **When** to trigger incident response (quantified thresholds)
- **Who** gets notified and how quickly

This plan covers all AI systems in scope of the AIMS:
- VoiceGuard Platform (AI voice agent for security)
- RMF Navigator (compliance assistant)
- VISTA (Naval defect detection)

---

## 2. Monitoring Systems by AI System

### 2.1 VoiceGuard Platform

| Monitoring Layer | Detection Method | Alert Threshold | Frequency |
|------------------|------------------|-----------------|-----------|
| **Uptime Monitoring** | Vapi dashboard API + ElevenLabs status page poll | Service unavailable for 2 consecutive checks | Every 5 minutes |
| **Error Rate Monitoring** | Vapi analytics API (failed calls / total calls) | >5% error rate sustained for 10 minutes | Real-time (API poll every 5 min) |
| **Latency Monitoring** | Vapi call duration metrics | Average response time >3 seconds for 5+ minutes | Every 5 minutes |
| **Bias Detection** | Fairness testing on call transcript samples | Statistical disparity >10% across demographic groups | Quarterly manual review |
| **Data Leak Detection** | ElevenLabs usage logs analysis | Anomalous voice clone requests or unauthorized data patterns | Monthly log review |
| **Client Complaint Channel** | Direct email to ceo@12thhouse.ai or phone hotline | Any complaint related to AI behavior | As received |

**Tools Used:**
- Vapi Dashboard & Analytics API
- ElevenLabs Console & API logs
- Better Uptime (status page monitoring)
- AWS CloudWatch (for backend health)

---

### 2.2 RMF Navigator

| Monitoring Layer | Detection Method | Alert Threshold | Frequency |
|------------------|------------------|-----------------|-----------|
| **Accuracy Monitoring** | Spot-check of AI outputs vs NIST SP 800-53/RMF source material | >2 inaccuracies in 10 sample outputs | Weekly manual review |
| **Hallucination Detection** | User feedback "Flag Output" button + manual review of flagged items | Any flagged output or pattern of unverifiable claims | Real-time + weekly review |
| **Security Monitoring** | AWS CloudTrail access logs + application authentication logs | Unauthorized access attempts, unusual access patterns | Weekly log review |
| **Model Performance** | Application response time logging via CloudWatch | p95 latency >5 seconds or error rate >1% | Real-time (CloudWatch alarms) |
| **Compliance Drift** | Comparison of outputs against updated NIST guidance | References to outdated control versions or deprecated frameworks | Monthly review |

**Tools Used:**
- AWS CloudTrail & CloudWatch
- RMF Navigator Admin Dashboard
- Anthropic Console (Claude API usage/performance)

---

### 2.3 VISTA (Naval Defect Detection)

| Monitoring Layer | Detection Method | Alert Threshold | Frequency |
|------------------|------------------|-----------------|-----------|
| **False Negative Rate** | Comparison of model-detected defects vs manual inspection samples | >2% missed defects in sample set | Monthly manual review |
| **False Positive Rate** | Tracking unnecessary manual reviews triggered by model | >15% false positive rate on defect classification | Monthly analysis |
| **Model Drift** | Quarterly evaluation on held-out test dataset | Accuracy drop >3% vs baseline model | Quarterly re-evaluation |
| **Processing Time** | Inference latency monitoring via application metrics | Inference time >2x baseline average (>4 seconds per image) | Real-time alerting |
| **Integration Health** | API endpoint health checks (UptimeRobot) | Endpoint down for >5 minutes or error rate >2% | Every 5 minutes |
| **Data Quality** | Input image validation logs | Corrupted inputs or format errors >1% | Weekly review |

**Tools Used:**
- AWS CloudWatch (for ML inference metrics)
- UptimeRobot (API monitoring)
- Custom evaluation pipeline (test dataset)
- Manual inspection records (Navy QA team)

---

## 3. Incident Detection Matrix

| Incident Type | Detection Method | Detection Source/System | Alert Threshold | Response Time Target | Notification Method |
|---------------|------------------|------------------------|-----------------|----------------------|---------------------|
| **Data Breach** | Log analysis + Anomaly detection | AWS CloudTrail, ElevenLabs logs, Application access logs | Unauthorized data access or exfiltration detected | 15 minutes | SMS → Email → Phone |
| **Bias Detection** | Statistical testing + User reports | Fairness testing scripts, Client complaints, User feedback | Measured bias >10% disparity OR bias complaint received | 4 hours | Email → Slack |
| **System Failure** | Health checks + Error rate monitoring | Better Uptime, Vapi dashboard, CloudWatch alarms | Service down >5 min OR error rate >5% for 10 min | 5 minutes | SMS → Slack → Email |
| **Adversarial Attack** | Input validation + Anomaly detection | Application logs, API rate limiting, Security scanning | Suspicious input patterns OR rate limit exceeded OR reported adversarial inputs | 30 minutes | Email → Slack |
| **Non-compliance** | Output auditing + Regulatory monitoring | Manual spot-checks, Regulatory update alerts, Client feedback | AI output violates NIST/DoD guidance OR regulatory requirements change | 24 hours | Email → Scheduled meeting |
| **Hallucination / Misinformation** | User feedback + Accuracy testing | Flag Output button, Weekly spot-checks | User flags output OR accuracy review finds unverifiable claims | 2 hours | Slack → Email |
| **Model Drift / Degradation** | Performance testing + Quality metrics | Evaluation pipelines, Accuracy tracking | Performance drop >3% vs baseline | 1 week (next review cycle) | Email → Jira ticket |
| **Unauthorized Access** | Access logging + Authentication monitoring | AWS CloudTrail, Application auth logs | Failed login attempts >5 in 10 min OR access from unknown IP | 15 minutes | SMS → Email |

---

## 4. Alerting & Escalation

### 4.1 Notification Channels

| Channel | Purpose | Tools |
|---------|---------|-------|
| **SMS** | Critical incidents requiring immediate response | Twilio (configured for on-call engineer) |
| **Slack** | Real-time team alerts and coordination | #ai-incidents channel |
| **Email** | Standard incident notifications and documentation | ai-safety@12thhouse.ai distribution list |
| **Phone** | Escalation for unresolved critical incidents | CEO direct line (after-hours) |
| **Jira** | Incident tracking and documentation | AI Safety project board |

### 4.2 Escalation Matrix

| Incident Level | Definition | First Response | Escalation Timeline |
|----------------|------------|----------------|---------------------|
| **Critical** | Data breach, System-wide outage, Active adversarial attack, Severe bias affecting users | AI Engineer (on-call) | If unresolved in 30 min → CTO → If unresolved in 2 hrs → CEO |
| **High** | Significant accuracy degradation, Hallucination reports, Security anomalies | AI Safety Officer | If unresolved in 4 hrs → CTO |
| **Medium** | Model drift detected, Minor performance issues, Non-compliance concerns | AI Engineer | If unresolved in 24 hrs → AI Safety Officer |
| **Low** | Documentation gaps, Review findings requiring follow-up | AI Safety Officer | Weekly review meeting |

### 4.3 Contact Information

| Role | Primary Contact | Escalation Contact |
|------|-----------------|-------------------|
| AI Engineer (On-call) | oncall@12thhouse.ai | - |
| AI Safety Officer | safety@12thhouse.ai | CTO |
| CTO | cto@12thhouse.ai | CEO |
| CEO | ceo@12thhouse.ai | - |

---

## 5. Response Procedures

### 5.1 Data Breach Response

1. **Immediate (0-15 min):** 
   - Acknowledge alert and assess scope via CloudTrail logs
   - Notify AI Safety Officer via SMS
   - Isolate affected systems if ongoing

2. **Short-term (15 min - 2 hrs):**
   - Document incident in Jira
   - If confirmed breach, invoke Data Breach Response Plan
   - Notify affected clients per contractual obligations

3. **Follow-up:**
   - Root cause analysis within 48 hours
   - Implement corrective actions
   - Update risk register

### 5.2 Bias Detection Response

1. **Immediate (0-4 hrs):**
   - Review flagged output or test results
   - Determine if bias is confirmed (requires human review)
   - Document in Jira

2. **Short-term (4-24 hrs):**
   - If confirmed, assess impact on affected users
   - Implement temporary mitigation (e.g., human review layer)
   - Notify AI Safety Officer

3. **Long-term:**
   - Retrain or fine-tune model with bias mitigation
   - Update fairness testing procedures

### 5.3 System Failure Response

1. **Immediate (0-5 min):**
   - Verify system status via monitoring dashboards
   - Check third-party service status (Vapi, ElevenLabs, Anthropic)
   - Notify team via Slack #ai-incidents

2. **Short-term (5-30 min):**
   - If third-party issue, engage vendor support
   - If internal issue, begin troubleshooting
   - Post status update to client status page if applicable

3. **Resolution:**
   - Document root cause
   - Update runbooks if needed

### 5.4 Adversarial Attack Response

1. **Immediate (0-30 min):**
   - Review suspicious inputs/activity
   - Block offending IPs/API keys if malicious
   - Enable enhanced logging

2. **Investigation (30 min - 24 hrs):**
   - Analyze attack vectors
   - Assess if model outputs were compromised
   - Document findings

3. **Remediation:**
   - Implement input validation improvements
   - Update threat model
   - Consider retraining with adversarial examples

### 5.5 Non-Compliance Response

1. **Discovery:**
   - Document non-compliance finding
   - Assess scope (how many outputs affected, which clients)

2. **Remediation (within 1 week):**
   - Update system prompts or model configuration
   - Re-audit affected outputs
   - Notify affected stakeholders

3. **Prevention:**
   - Update monitoring to catch similar issues
   - Review compliance requirements against current implementation

### 5.6 Hallucination Response

1. **Immediate (0-2 hrs):**
   - Review flagged output for accuracy
   - Remove or correct if confirmed hallucination
   - Thank user for flagging

2. **Analysis:**
   - Identify pattern (one-off or systemic)
   - If systemic, initiate model review

3. **Improvement:**
   - Update RAG sources or grounding procedures
   - Enhance prompt engineering

---

## 6. Review & Maintenance

### 6.1 Review Schedule

| Review Type | Frequency | Owner | Purpose |
|-------------|-----------|-------|---------|
| **Metrics Review** | Weekly | AI Engineer | Review monitoring dashboards, tune thresholds |
| **Incident Triage** | Weekly | AI Safety Officer | Review open incidents, validate detection efficacy |
| **Plan Review** | Quarterly | AI Safety Officer | Update monitoring coverage, tools, thresholds based on lessons learned |
| **Audit Alignment** | Annually | CTO | Ensure monitoring meets ISO 42001 and client audit requirements |

### 6.2 Maintenance Triggers

This plan must be updated when:

- **New AI System Deployed:** Add monitoring section within 2 weeks of production deployment
- **Monitoring Tool Changes:** Update references if switching from Vapi, ElevenLabs, Better Uptime, etc.
- **Threshold Tuning:** Document any threshold changes with rationale
- **Post-Incident:** Incorporate lessons learned within 1 week of significant incident
- **Regulatory Changes:** Update when new compliance requirements affect monitoring

### 6.3 Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | January 2026 | AI Safety Officer | Initial release |

---

## Appendix A: Monitoring Tools Reference

| Tool | Purpose | Access URL | Primary Contact |
|------|---------|------------|-----------------|
| Vapi Dashboard | Voice agent monitoring | https://dashboard.vapi.ai | AI Engineer |
| ElevenLabs Console | Voice synthesis logs | https://elevenlabs.io/app | AI Engineer |
| Better Uptime | Status page monitoring | https://betteruptime.com | AI Engineer |
| AWS CloudWatch | Infrastructure metrics | AWS Console | AI Engineer |
| AWS CloudTrail | Security auditing | AWS Console | AI Engineer + CTO |
| Anthropic Console | Claude API usage | https://console.anthropic.com | AI Engineer |
| UptimeRobot | API endpoint monitoring | https://uptimerobot.com | AI Engineer |

---

## Appendix B: Related Documents

- AIMS Policy Section 11 (Incident Response)
- Data Breach Response Plan
- AI Risk Register
- VoiceGuard System Documentation
- RMF Navigator System Documentation
- VISTA System Documentation

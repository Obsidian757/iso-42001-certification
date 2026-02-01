# AI Impact Assessment Template

**12th House AI - ISO/IEC 42001:2023 Compliance**

---

## Assessment Information

**AI System Name:** _________________________________

**Assessment Date:** _________________________________

**Assessor:** _________________________________

**System Owner:** _________________________________

**Deployment Status:** ☐ Planned  ☐ Development  ☐ Pilot  ☐ Production

---

## 1. System Description

### 1.1 Purpose
*What problem does this AI system solve? What is its intended function?*

_______________________________________________________________________________

_______________________________________________________________________________

### 1.2 Technology
*What AI technology is used? (e.g., voice AI, LLM, machine learning model, etc.)*

_______________________________________________________________________________

### 1.3 Third-Party Components
*List any third-party AI services or models (ElevenLabs, Claude, Vapi, etc.)*

_______________________________________________________________________________

### 1.4 Data Sources
*What data does the AI use? Where does it come from?*

_______________________________________________________________________________

### 1.5 Decision Scope
*What decisions or recommendations does the AI make? Are they fully automated or human-reviewed?*

☐ Fully automated (no human review)  
☐ Human-in-the-loop (AI recommends, human decides)  
☐ Human-on-the-loop (human monitors, can override)

_______________________________________________________________________________

---

## 2. Stakeholder Analysis

### 2.1 Who is affected by this AI system?

☐ End users (customers, citizens)  
☐ Clients/business partners  
☐ Employees  
☐ Public/society  
☐ Regulators  
☐ Other: _________________________________

### 2.2 Are vulnerable populations involved?

☐ Children  
☐ Elderly  
☐ People with disabilities  
☐ Low-income individuals  
☐ Minorities  
☐ None  

---

## 3. Risk & Impact Assessment

### 3.1 Privacy & Data Protection

**Question:** Does the AI process personal information (PII), protected health information (PHI), or controlled unclassified information (CUI)?

☐ Yes  ☐ No

**If yes, what data protection measures are in place?**

☐ Encryption in transit and at rest  
☐ Data minimization (collect only necessary data)  
☐ Access controls  
☐ Retention limits and auto-deletion  
☐ Business Associate Agreement (for HIPAA)  
☐ User consent mechanisms  
☐ Other: _________________________________

**Privacy Risk Level:**  ☐ Low  ☐ Medium  ☐ High  ☐ Critical

---

### 3.2 Fairness & Bias

**Question:** Could the AI treat different groups of people differently (by race, gender, age, accent, etc.)?

☐ Yes  ☐ No  ☐ Unknown

**If yes, what bias mitigation measures are in place?**

☐ Tested with diverse data samples  
☐ Ongoing monitoring for differential outcomes  
☐ Human review for high-stakes decisions  
☐ Known limitations documented  
☐ Appeal/override mechanisms  
☐ Other: _________________________________

**Bias Risk Level:**  ☐ Low  ☐ Medium  ☐ High  ☐ Critical

---

### 3.3 Safety & Reliability

**Question:** What happens if the AI fails or makes an error?

☐ Minor inconvenience  
☐ Service disruption (recoverable)  
☐ Financial loss  
☐ Reputational damage  
☐ Physical harm  
☐ Legal/regulatory consequences

**What safety measures are in place?**

☐ Performance testing before deployment  
☐ Continuous monitoring  
☐ Graceful degradation (fallback to human)  
☐ Incident response playbook  
☐ Regular model retraining/updates  
☐ Uptime SLAs  
☐ Other: _________________________________

**Safety Risk Level:**  ☐ Low  ☐ Medium  ☐ High  ☐ Critical

---

### 3.4 Transparency & Explainability

**Question:** Can users understand how the AI makes decisions?

☐ Yes, fully explainable  
☐ Partially explainable  
☐ Black box (not explainable)

**What transparency measures are in place?**

☐ User notification that AI is involved  
☐ "Why" explanations for AI decisions  
☐ Documentation of AI logic  
☐ Audit trails  
☐ Human appeal process  
☐ Other: _________________________________

**Transparency Risk Level:**  ☐ Low  ☐ Medium  ☐ High  ☐ Critical

---

### 3.5 Security

**Question:** Could the AI be manipulated or attacked (e.g., prompt injection, adversarial inputs)?

☐ Yes  ☐ No  ☐ Unknown

**What security measures are in place?**

☐ Input validation and sanitization  
☐ Output filtering (block sensitive data)  
☐ Access controls (least privilege)  
☐ Rate limiting  
☐ Logging and monitoring  
☐ Security testing (red team)  
☐ Other: _________________________________

**Security Risk Level:**  ☐ Low  ☐ Medium  ☐ High  ☐ Critical

---

### 3.6 Legal & Regulatory Compliance

**Question:** What regulations apply to this AI system?

☐ OMB M-25-21 / M-25-22 (federal AI use)  
☐ NIST AI RMF  
☐ DFARS / CMMC (defense contractors)  
☐ HIPAA (healthcare)  
☐ FERPA (education)  
☐ GDPR / EU AI Act (international)  
☐ FedRAMP / IL5 (government cloud)  
☐ Other: _________________________________

**Are all applicable compliance requirements met?**

☐ Yes  ☐ No  ☐ In progress

**If no, what gaps exist?**

_______________________________________________________________________________

**Compliance Risk Level:**  ☐ Low  ☐ Medium  ☐ High  ☐ Critical

---

### 3.7 Ethical Considerations

**Question:** Could this AI be used unethically (surveillance, manipulation, discrimination)?

☐ Yes  ☐ No

**If yes, what safeguards are in place?**

☐ Acceptable Use Policy in contracts  
☐ Ethical AI training for users  
☐ Usage monitoring and audit trails  
☐ Right to suspend service for misuse  
☐ Contractual liability protections  
☐ Other: _________________________________

**Ethical Risk Level:**  ☐ Low  ☐ Medium  ☐ High  ☐ Critical

---

## 4. Overall Risk Summary

**Highest Risk Area:** _________________________________

**Overall Risk Rating:**  ☐ Low  ☐ Medium  ☐ High  ☐ Critical

**Risk Calculation:**
- If any area is Critical → Overall = Critical
- If any area is High → Overall = High
- If multiple Medium → Overall = High
- Otherwise → Overall = Medium or Low

---

## 5. Mitigation Plan

**For each High or Critical risk identified above, document mitigation plan:**

| Risk Area | Risk Description | Mitigation Action | Owner | Deadline | Status |
|-----------|------------------|-------------------|-------|----------|--------|
|           |                  |                   |       |          |        |
|           |                  |                   |       |          |        |
|           |                  |                   |       |          |        |

---

## 6. Decision

**Can this AI system be deployed as currently designed?**

☐ **Approved** - Proceed with deployment (Low or Medium risk with controls)  
☐ **Conditional Approval** - Proceed with enhanced monitoring (High risk with mitigation)  
☐ **Rejected** - Do not deploy until risks reduced (Critical risk)  
☐ **Requires Further Review** - Escalate to leadership

**Approver:** _________________________________  
**Signature:** _________________________________  
**Date:** _________________________________

---

## 7. Post-Deployment Monitoring

**For approved systems, define ongoing monitoring:**

| Metric | Target | Frequency | Alert Threshold |
|--------|--------|-----------|-----------------|
| Uptime | 99.5% | Real-time | <99% |
| Error Rate | <1% | Daily | >2% |
| Bias Incidents | 0 | Weekly | >0 |
| Privacy Breaches | 0 | Real-time | >0 |
| Security Events | 0 | Real-time | >0 |

**Next Review Date:** _________________________________

---

## 8. Documentation & Record Keeping

**Attach or reference supporting documentation:**

☐ AI system design documentation  
☐ Data flow diagram  
☐ Security assessment  
☐ Compliance checklist  
☐ Testing results  
☐ User training materials  
☐ Third-party vendor agreements  
☐ Other: _________________________________

---

**Template Version:** 1.0  
**Last Updated:** February 1, 2026

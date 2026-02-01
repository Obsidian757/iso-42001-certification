# 12th House AI - AI Risk Register

**Document Control**
- Version: 1.0
- Last Updated: February 1, 2026
- Owner: Brannon Solomon (AI Risk Owner)
- Review Frequency: Quarterly (or after significant incidents)

---

## Risk Rating Matrix

**Likelihood:**
- **Rare (1):** < 5% chance in next 12 months
- **Unlikely (2):** 5-25% chance
- **Possible (3):** 25-50% chance
- **Likely (4):** 50-75% chance
- **Almost Certain (5):** > 75% chance

**Impact:**
- **Negligible (1):** Minor inconvenience, no business impact
- **Minor (2):** Limited impact, easily recovered
- **Moderate (3):** Significant disruption, reputational concern
- **Major (4):** Serious harm, regulatory scrutiny, major client loss
- **Catastrophic (5):** Permanent business damage, legal liability, harm to people

**Risk Score = Likelihood × Impact**

| Score | Risk Level | Action Required |
|-------|-----------|-----------------|
| 1-4 | Low | Monitor, accept |
| 5-9 | Medium | Standard controls |
| 10-14 | High | Mitigation plan required |
| 15-25 | Critical | Must eliminate or CEO approval to accept |

---

## Active Risks

### RISK-001: Third-Party AI Data Leakage

**Category:** Privacy & Data Protection  
**Affected Systems:** VoiceGuard (uses ElevenLabs, Vapi), RMF Navigator, consulting work using Claude

**Description:**
Client data (including CUI, PII, or proprietary information) is inadvertently shared with third-party AI providers (ElevenLabs, Claude, Vapi, etc.) without proper safeguards, leading to unauthorized disclosure.

**Likelihood:** Possible (3)  
**Impact:** Major (4)  
**Risk Score:** 12 (High)

**Treatment Strategy:** Reduce

**Mitigation Measures:**
1. Use enterprise/business tier AI services with data protection agreements (not free consumer tiers)
2. Never input CUI or client confidential data into unapproved AI tools
3. Configure third-party AI with "do not train" policies where available
4. Maintain data flow diagram documenting what data goes to which vendor
5. Annual vendor security reviews
6. Client contracts specify data handling for AI tools

**Residual Risk:** Medium (6) - Likelihood reduced to Unlikely (2), Impact remains Major (4)

**Owner:** Brannon Solomon (Technical Lead)  
**Status:** Controls in place, monitoring ongoing  
**Next Review:** May 1, 2026

---

### RISK-002: Algorithmic Bias in Voice AI

**Category:** Fairness & Bias  
**Affected Systems:** VoiceGuard voice agents (appointment setting, customer service)

**Description:**
Voice AI systems exhibit bias based on accent, dialect, speech patterns, or demographic characteristics, leading to differential service quality and potential discrimination claims.

**Likelihood:** Possible (3)  
**Impact:** Moderate (3)  
**Risk Score:** 9 (Medium)

**Treatment Strategy:** Reduce

**Mitigation Measures:**
1. Test voice agents with diverse voice samples (accents, ages, dialects)
2. Monitor call handling metrics by demographic where ethically available
3. Provide human escalation path for all voice interactions
4. Document known limitations in VoiceGuard deployments
5. Client training on bias monitoring
6. Regular performance audits for fairness

**Residual Risk:** Low (4) - Likelihood reduced to Unlikely (2), Impact remains Moderate (3) but containable

**Owner:** Brannon Solomon (Technical Lead)  
**Status:** Active monitoring, controls partially implemented  
**Next Review:** March 1, 2026 (post-deployment testing)

---

### RISK-003: Regulatory Non-Compliance (OMB Memos)

**Category:** Compliance & Legal  
**Affected Systems:** All client AI engagements

**Description:**
Failure to stay current with evolving federal AI regulations (OMB M-25-21, M-25-22, M-26-04, NIST updates) results in client non-compliance, contract breach, or loss of credibility.

**Likelihood:** Unlikely (2)  
**Impact:** Major (4)  
**Risk Score:** 8 (Medium)

**Treatment Strategy:** Reduce

**Mitigation Measures:**
1. Subscribe to federal register updates (OMB, NIST, DoD AI)
2. Quarterly regulatory review and framework updates
3. Maintain ISO 42001 certification (forces compliance discipline)
4. Participate in NavalX and industry forums for early awareness
5. Document regulatory assumptions in all client engagements
6. Include change order provisions for regulatory shifts

**Residual Risk:** Low (4) - Likelihood remains Unlikely (2), Impact reduced to Minor (2) via proactive monitoring

**Owner:** Brannon Solomon (Compliance Officer)  
**Status:** Monitoring in place  
**Next Review:** May 1, 2026

---

### RISK-004: Voice AI PII Exposure (HIPAA/FERPA)

**Category:** Privacy & Data Protection  
**Affected Systems:** VoiceGuard in healthcare and education contexts

**Description:**
Voice agents collect or process personally identifiable information (PII) or protected health information (PHI) in violation of HIPAA, FERPA, or other privacy regulations, resulting in regulatory penalties or client liability.

**Likelihood:** Possible (3)  
**Impact:** Catastrophic (5)  
**Risk Score:** 15 (Critical)

**Treatment Strategy:** Reduce (must reduce to High or lower before deployment)

**Mitigation Measures:**
1. **Business Associate Agreements (BAA)** with all voice AI vendors for healthcare clients
2. PII minimization - voice agents collect only essential data points
3. Encryption in transit and at rest for all voice data
4. Retention policies - auto-delete recordings after defined period
5. User consent and notification ("This call may be recorded")
6. Access controls - limit who can access voice data
7. Annual HIPAA/FERPA compliance audits for relevant engagements
8. Avoid deploying voice AI for sensitive use cases until controls validated

**Residual Risk:** High (12) - Likelihood reduced to Unlikely (2), but Impact remains Major (4) if it occurs

**Owner:** Brannon Solomon (AI Risk Owner)  
**Status:** **CRITICAL - Enhanced controls required before healthcare/education deployments**  
**Next Review:** Immediate (before any HIPAA/FERPA engagement)

---

### RISK-005: AI System Availability/Outage

**Category:** Reliability & Safety  
**Affected Systems:** VoiceGuard, RMF Navigator, client production deployments

**Description:**
AI system failure, API downtime (ElevenLabs, Claude), or configuration errors cause service outage, disrupting client operations and damaging reputation.

**Likelihood:** Likely (4)  
**Impact:** Moderate (3)  
**Risk Score:** 12 (High)

**Treatment Strategy:** Reduce + Share (via SLAs)

**Mitigation Measures:**
1. Use redundant API providers where feasible (multi-vendor strategy)
2. Implement graceful degradation (fallback to human agents if AI fails)
3. Real-time monitoring and alerting for production AI systems
4. Documented incident response playbook
5. Client SLAs set realistic uptime expectations (99%, not 99.9%)
6. Maintain backup capacity for critical workloads
7. Regular disaster recovery testing

**Residual Risk:** Medium (6) - Likelihood reduced to Unlikely (2), Impact remains Moderate (3)

**Owner:** Brannon Solomon (Technical Lead)  
**Status:** Monitoring and alerting in progress  
**Next Review:** April 1, 2026

---

### RISK-006: Adversarial Manipulation (Prompt Injection)

**Category:** Security  
**Affected Systems:** VoiceGuard, any AI accepting user input

**Description:**
Malicious user manipulates AI through prompt injection, jailbreaking, or adversarial inputs to extract sensitive data, bypass security, or cause harmful outputs.

**Likelihood:** Possible (3)  
**Impact:** Moderate (3)  
**Risk Score:** 9 (Medium)

**Treatment Strategy:** Reduce

**Mitigation Measures:**
1. Input validation and sanitization for all user inputs to AI
2. Role-based access controls - AI has minimum necessary permissions
3. Output filtering - detect and block sensitive data in AI responses
4. Rate limiting to prevent automated attack attempts
5. Logging and monitoring for suspicious AI interactions
6. Regular security testing (red team exercises)
7. Keep third-party AI models updated with latest security patches

**Residual Risk:** Medium (6) - Likelihood reduced to Unlikely (2), Impact remains Moderate (3)

**Owner:** Brannon Solomon (Technical Lead)  
**Status:** Controls in design phase  
**Next Review:** March 15, 2026

---

### RISK-007: Client Misuse of AI Tools

**Category:** Ethical & Governance  
**Affected Systems:** Client-deployed VoiceGuard instances, consulting deliverables

**Description:**
Client uses 12th House AI-delivered tools for unethical purposes (discrimination, surveillance, manipulation) without 12th House AI's knowledge, causing reputational damage or legal liability.

**Likelihood:** Unlikely (2)  
**Impact:** Major (4)  
**Risk Score:** 8 (Medium)

**Treatment Strategy:** Reduce + Transfer (via contracts)

**Mitigation Measures:**
1. **Acceptable Use Policy** in all client contracts
2. Ethical AI training for client teams during deployment
3. Built-in audit trails for client AI usage
4. Contractual right to suspend service for misuse
5. Liability limitations in master services agreements
6. Client attestation of compliance with ethical AI principles
7. Periodic compliance checks for high-risk use cases

**Residual Risk:** Low (4) - Likelihood remains Unlikely (2), Impact reduced to Minor (2) via contractual protections

**Owner:** Brannon Solomon (Leadership)  
**Status:** Contract language in development  
**Next Review:** March 1, 2026 (with legal review)

---

### RISK-008: Model Degradation (Data Drift)

**Category:** Performance & Reliability  
**Affected Systems:** VoiceGuard (if using custom models), RMF Navigator

**Description:**
AI models degrade over time due to data drift, changing user behavior, or environmental shifts, leading to reduced accuracy and client dissatisfaction.

**Likelihood:** Likely (4)  
**Impact:** Minor (2)  
**Risk Score:** 8 (Medium)

**Treatment Strategy:** Accept with monitoring

**Mitigation Measures:**
1. Performance baselines established at deployment
2. Continuous monitoring of accuracy, response quality, error rates
3. Quarterly model review and retraining assessment
4. Client communication when performance degrades
5. Version control for AI models with rollback capability
6. A/B testing for model updates

**Residual Risk:** Low (4) - Likelihood reduced to Unlikely (2), Impact remains Minor (2)

**Owner:** Brannon Solomon (Technical Lead)  
**Status:** Monitoring framework in design  
**Next Review:** May 1, 2026

---

### RISK-009: Lack of AI Explainability

**Category:** Transparency  
**Affected Systems:** All AI systems, especially high-stakes decisions

**Description:**
AI makes decisions (e.g., appointment denials, risk assessments) that cannot be explained to users or auditors, violating transparency requirements or eroding user trust.

**Likelihood:** Possible (3)  
**Impact:** Moderate (3)  
**Risk Score:** 9 (Medium)

**Treatment Strategy:** Reduce

**Mitigation Measures:**
1. Select interpretable AI models where high-stakes decisions involved
2. Implement "why" explanations for AI decisions (explainability layer)
3. Human review for high-impact AI outputs
4. Document AI logic and decision criteria
5. Provide users with appeal/override mechanisms
6. Audit trails capturing AI decision rationale

**Residual Risk:** Medium (6) - Likelihood reduced to Unlikely (2), Impact remains Moderate (3)

**Owner:** Brannon Solomon (Technical Lead)  
**Status:** Explainability features in roadmap  
**Next Review:** April 1, 2026

---

### RISK-010: Vendor Lock-In (Third-Party AI Dependency)

**Category:** Business Continuity  
**Affected Systems:** All systems using ElevenLabs, Vapi, Claude, OpenRouter

**Description:**
Over-reliance on single third-party AI vendor creates business continuity risk if vendor raises prices, changes terms, suffers outage, or exits market.

**Likelihood:** Possible (3)  
**Impact:** Moderate (3)  
**Risk Score:** 9 (Medium)

**Treatment Strategy:** Reduce

**Mitigation Measures:**
1. Multi-vendor strategy - use multiple AI providers where feasible
2. Abstraction layers - avoid tight coupling to single vendor API
3. Data portability - ensure ability to migrate to new vendors
4. Monitor vendor health and alternatives
5. Maintain internal expertise on multiple AI platforms
6. Contract terms allow termination and data export

**Residual Risk:** Medium (6) - Likelihood reduced to Unlikely (2), Impact remains Moderate (3)

**Owner:** Brannon Solomon (Leadership)  
**Status:** Architecture supports multi-vendor  
**Next Review:** June 1, 2026

---

## Risk Summary Dashboard

| Risk Level | Count | Percentage |
|------------|-------|------------|
| Critical   | 1     | 10%        |
| High       | 2     | 20%        |
| Medium     | 6     | 60%        |
| Low        | 1     | 10%        |

**Total Active Risks:** 10

**Risks Requiring Immediate Action:**
- RISK-004: Voice AI PII Exposure (Critical) - **Enhanced controls before healthcare/education deployments**

---

## Risk Review Schedule

- **Quarterly Review:** Next scheduled May 1, 2026
- **Triggered Review:** After any High/Critical incident
- **Annual Deep Dive:** February 2027 (full risk landscape reassessment)

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| Feb 1, 2026 | Initial risk register created for ISO 42001 certification | Brannon Solomon |

# 12th House AI - Third-Party AI Vendor Management

**Document Control**
- Version: 1.0
- Effective Date: February 1, 2026
- Owner: Brannon Solomon (Technical Lead)
- Next Review: February 1, 2027

---

## 1. Purpose

This procedure establishes requirements for selecting, managing, and monitoring third-party AI vendors to ensure compliance with ISO/IEC 42001:2023 (Clause 8.6), NIST AI RMF, and federal requirements including EO 14110 which holds contractors liable for third-party AI compliance.

---

## 2. Scope

This procedure applies to all third-party AI technologies used by 12th House AI, including:
- AI APIs and services (Claude, ElevenLabs, Vapi, OpenRouter)
- AI models and frameworks (pre-trained models, embeddings)
- AI-enabled software platforms (Azure AI)
- AI components in broader solutions (AI features in SaaS products)

---

## 3. Current Third-Party AI Vendor Inventory

### Active Vendors

| Vendor | Service | Classification | Data Allowed | Annual Cost | Contract Status | Last Review |
|--------|---------|----------------|--------------|-------------|-----------------|-------------|
| **Anthropic (Claude)** | LLM API, Claude Code | Enterprise | Internal, Confidential | ~$1,200/yr | Business tier | Jan 2026 |
| **ElevenLabs** | Voice synthesis | Business | Internal, Confidential | ~$600/yr | Business tier | Jan 2026 |
| **Vapi** | Voice agent platform | Business | Internal, Confidential | ~$480/yr | Business tier | Jan 2026 |
| **OpenRouter** | Multi-model API gateway | Standard | Public, Internal | ~$200/yr | Standard | Jan 2026 |
| **Microsoft Azure AI** | Cloud AI services | Enterprise | All (commercial) | Variable | EA agreement | Jan 2026 |
| **OpenAI** | GPT models (via Azure) | Enterprise | Per Azure controls | Via Azure | Azure Marketplace | Jan 2026 |

### Conditional/Restricted Vendors

| Vendor | Status | Restriction | Action Required |
|--------|--------|-------------|-----------------|
| **Any free-tier AI** | Prohibited for production | No client or sensitive data | Use business/enterprise tiers only |
| **ChatGPT free** | Prohibited for work | No work data | Do not use for client work |
| **Consumer AI apps** | Case-by-case | Evaluate per use case | Risk assessment before use |

---

## 4. Vendor Selection Criteria

### 4.1 Mandatory Requirements

All third-party AI vendors must meet these criteria before approval:

**Security:**
- [ ] SOC 2 Type II certification (or equivalent)
- [ ] Encryption at rest and in transit (AES-256 minimum)
- [ ] Access controls and authentication (SSO/SAML preferred)
- [ ] Incident response process documented
- [ ] Regular security testing/pen testing

**Privacy:**
- [ ] Data Processing Agreement (DPA) available
- [ ] GDPR/CCPA compliance documented
- [ ] "Do not train on customer data" policy or opt-out available
- [ ] Data residency options (U.S. required for federal work)
- [ ] Data deletion capabilities

**Transparency:**
- [ ] AI model capabilities and limitations documented
- [ ] Known biases and failure modes disclosed
- [ ] Version control and change notification
- [ ] SLA and support terms clear

**Compliance:**
- [ ] FedRAMP authorization (for federal work)
- [ ] HIPAA BAA available (for healthcare use cases)
- [ ] Terms allow use for intended purpose

### 4.2 Preferred Requirements

Nice-to-have features that increase vendor score:

- Model explainability features
- Audit logging and access to logs
- Customization/fine-tuning options
- Multi-region deployment
- 24/7 support availability
- API rate limits suitable for production
- Cost transparency and predictability

### 4.3 Vendor Scoring

Score each vendor 1-5 on these dimensions:

| Dimension | Weight | Score (1-5) | Weighted |
|-----------|--------|-------------|----------|
| Security posture | 25% | ___ | ___ |
| Privacy controls | 20% | ___ | ___ |
| Compliance coverage | 20% | ___ | ___ |
| Technical capability | 15% | ___ | ___ |
| Cost effectiveness | 10% | ___ | ___ |
| Support quality | 10% | ___ | ___ |
| **Total** | 100% | | ___ / 5.0 |

**Approval thresholds:**
- 4.0+: Approved for all use cases
- 3.0-3.9: Approved with conditions (document limitations)
- 2.0-2.9: Approved for low-risk use only
- <2.0: Not approved

---

## 5. Vendor Approval Process

### 5.1 New Vendor Request

1. **Business justification:** Why is this vendor needed? What alternatives were considered?
2. **Technical assessment:** Does vendor meet mandatory requirements?
3. **Contract review:** Are terms acceptable? DPA in place?
4. **Risk assessment:** What could go wrong? What data will be exposed?
5. **Approval decision:** Approve, approve with conditions, or reject

### 5.2 Approval Authority

| Vendor Risk Level | Approval Authority |
|-------------------|-------------------|
| Low (public data only) | Technical Lead (self-approval) |
| Medium (internal/confidential) | CEO approval required |
| High (regulated data) | CEO + legal review required |

### 5.3 Documentation

For each approved vendor, maintain:
- Vendor assessment scorecard
- Contract and DPA copies
- Approval record with date and approver
- Conditions or restrictions documented
- Annual review schedule

---

## 6. Vendor Contract Requirements

### 6.1 Minimum Contract Terms

All third-party AI vendor contracts must include:

**Data Protection:**
- Vendor will not train on customer data without explicit consent
- Data encrypted at rest and in transit
- Data deleted upon contract termination (with certification)
- Data localization (U.S. only for federal work)

**Security:**
- Security incident notification within 72 hours
- Right to audit upon request (annually minimum)
- Maintain SOC 2 or equivalent certification

**Compliance:**
- Comply with applicable laws (GDPR, CCPA, HIPAA if applicable)
- Cooperate with regulatory inquiries
- Indemnification for vendor-caused compliance failures

**Service:**
- Defined SLA (uptime, response time)
- 30-day notice for material changes
- Clear termination and exit provisions

### 6.2 HIPAA Business Associate Agreement (BAA)

For vendors processing PHI:
- Standard BAA executed before PHI processing
- Vendor listed as Business Associate in compliance documentation
- Annual confirmation of BAA status
- Incident response aligned with HIPAA timelines

**Current BAA Status:**

| Vendor | BAA Available? | BAA Executed? | Notes |
|--------|----------------|---------------|-------|
| ElevenLabs | Yes (Enterprise) | Pending | Required before healthcare deployments |
| Vapi | Unknown | No | Evaluate before healthcare use |
| Azure AI | Yes | Yes | Standard Microsoft HIPAA BAA |
| Claude | Yes (Enterprise) | Pending | Required for healthcare-related work |

### 6.3 Federal Contract Flow-Down

For vendors used in federal work:
- DFARS 252.204-7012 compliance required (CUI)
- FedRAMP High authorization (or equivalent)
- Made in U.S.A. requirements if applicable
- Security clearance for personnel accessing CUI

---

## 7. Ongoing Vendor Monitoring

### 7.1 Continuous Monitoring

**Daily/Automatic:**
- API availability and latency (monitoring dashboards)
- Error rates and anomalies
- Usage against quotas

**Weekly:**
- Review vendor security advisories
- Check for service announcements or changes
- Monitor vendor news for security incidents

**Monthly:**
- Usage and cost analysis
- Performance trends
- Compare against SLA commitments

### 7.2 Quarterly Vendor Review

For each active vendor, conduct quarterly review:

1. **Performance assessment:**
   - Uptime met SLA? (target: 99.5%+)
   - Incidents or outages?
   - Support responsiveness?

2. **Security update:**
   - Any reported vulnerabilities?
   - Certifications still current?
   - Policy changes?

3. **Cost review:**
   - Actual vs. budgeted spend
   - Cost optimization opportunities
   - Pricing changes

4. **Continuing need:**
   - Still using this vendor?
   - Better alternatives available?
   - Consolidation opportunities?

### 7.3 Annual Vendor Recertification

Annual recertification includes:
- Full vendor assessment scorecard refresh
- Contract review and renewal decision
- DPA/BAA confirmation
- Security certification verification
- Formal approval renewal

---

## 8. Vendor Risk Assessment

### 8.1 Risk Categories

| Risk | Description | Likelihood | Impact | Mitigation |
|------|-------------|------------|--------|------------|
| **Data breach at vendor** | Vendor security incident exposes client data | Medium | High | Encryption, DPA, incident response plan |
| **Service outage** | Vendor unavailable, impacting production | Medium | Medium | Multi-vendor strategy, graceful degradation |
| **Model degradation** | Vendor AI quality degrades | Low | Medium | Performance monitoring, alternative providers |
| **Pricing changes** | Vendor raises prices significantly | Medium | Medium | Budget buffer, multi-vendor options |
| **Policy changes** | Vendor changes terms of service | Medium | Low | 30-day notice requirement, contract terms |
| **Vendor exit** | Vendor discontinues service | Low | High | Data portability, abstraction layer |
| **Compliance failure** | Vendor fails regulatory requirement | Low | High | Due diligence, audit rights, indemnification |

### 8.2 Risk Mitigation Strategies

**Multi-Vendor Strategy:**
- Don't over-rely on single vendor for critical capabilities
- Maintain abstraction layers for easy vendor switching
- Keep alternatives evaluated and ready

**Data Protection:**
- Encrypt data before sending to vendors where possible
- Minimize data sent to vendors (data minimization)
- Use vendor data residency controls

**Contractual Protection:**
- Indemnification for vendor-caused failures
- Audit rights
- Exit provisions with data return/deletion
- Change notification requirements

**Technical Resilience:**
- Graceful degradation when vendor unavailable
- Caching and fallback mechanisms
- Regular backup of vendor-dependent configurations

---

## 9. Vendor Incident Management

### 9.1 Vendor Incident Triggers

**Immediate escalation required if vendor reports:**
- Security breach affecting customer data
- Unauthorized access to systems
- Service outage >4 hours
- Compliance certification loss
- Material terms of service changes

### 9.2 Response Procedure

1. **Assess impact:** What data/systems are affected?
2. **Communicate:** Notify affected clients if needed
3. **Contain:** Suspend vendor integration if necessary
4. **Document:** Record incident details and vendor response
5. **Recover:** Resume operations when vendor issue resolved
6. **Review:** Post-incident analysis, update risk assessment

### 9.3 Vendor Incident Log

Track all vendor incidents:
- Date and time
- Vendor name
- Incident description
- Impact to 12th House AI/clients
- Vendor response
- Resolution timeline
- Follow-up actions

---

## 10. Vendor Exit Management

### 10.1 Exit Triggers

- Contract expires and not renewing
- Vendor fails to meet requirements
- Better alternative available
- Vendor discontinues service
- Vendor acquired or exits market

### 10.2 Exit Procedure

1. **Notice:** Provide required notice per contract
2. **Data:** Request full data export in usable format
3. **Deletion:** Request vendor data deletion with written confirmation
4. **Transition:** Migrate to alternative vendor or internal solution
5. **Verification:** Confirm data deleted, access revoked
6. **Documentation:** Update vendor inventory, archive records

### 10.3 Data Portability Requirements

Before selecting vendors, confirm:
- Data can be exported in standard formats
- No proprietary lock-in for model weights or configurations
- Reasonable timeline for data export (30 days max)
- Written deletion confirmation available

---

## 11. Specific Vendor Profiles

### 11.1 Anthropic (Claude)

**Use:** Primary LLM for code generation, analysis, documentation

**Tier:** Business/Enterprise

**Data Allowed:** Public, Internal, Confidential (per DPA)

**DPA Status:** Yes, executed

**Security:** SOC 2 Type II, encryption, no training on prompts by default

**Restrictions:**
- No CUI without Azure deployment option
- No PHI without BAA (explore enterprise tier)

**Renewal Date:** Annual

**Alternative:** Azure OpenAI, Gemini

---

### 11.2 ElevenLabs

**Use:** Voice synthesis for VoiceGuard

**Tier:** Business

**Data Allowed:** Internal, Confidential (per DPA)

**DPA Status:** Yes

**Security:** SOC 2, encryption

**Restrictions:**
- No PHI until BAA executed
- Voice cloning requires explicit consent documentation
- Retain voice data per retention policy (30 days)

**HIPAA Ready:** Pending BAA execution

**Renewal Date:** Annual

**Alternative:** Azure Speech Services, Play.ht

---

### 11.3 Vapi

**Use:** Voice agent conversation platform for VoiceGuard

**Tier:** Business

**Data Allowed:** Internal, Confidential

**DPA Status:** In progress

**Security:** Encryption, access controls

**Restrictions:**
- No PHI until HIPAA compliance confirmed
- No CUI (not FedRAMP authorized)

**Renewal Date:** Annual

**Alternative:** Retell.ai, custom build with Twilio

---

### 11.4 OpenRouter

**Use:** Multi-model API gateway for flexible model access

**Tier:** Standard

**Data Allowed:** Public, Internal only

**DPA Status:** Standard terms

**Security:** Basic encryption, no advanced controls

**Restrictions:**
- Do NOT use for confidential or regulated data
- Use only for testing and non-sensitive workloads

**Alternative:** Direct provider APIs

---

### 11.5 Microsoft Azure AI Services

**Use:** Enterprise AI platform, GPT models, Cognitive Services

**Tier:** Enterprise Agreement

**Data Allowed:** All (commercial cloud)

**DPA Status:** Microsoft Online Services DPA

**Security:** SOC 2, ISO 27001, FedRAMP (GovCloud), HIPAA BAA available

**Compliance:**
- Standard commercial: SOC 2, HIPAA ready
- GovCloud: FedRAMP High, IL5, CUI approved

**Restrictions:**
- GovCloud required for CUI workloads
- Additional cost for Gov-specific services

**Renewal Date:** Per EA terms

**Alternative:** AWS AI, Google Cloud AI

---

## 12. Documentation and Records

Maintain the following vendor records:

- Vendor inventory (current list with status)
- Assessment scorecards (selection and annual)
- Contracts and DPAs
- BAAs (for HIPAA vendors)
- Incident log
- Quarterly review notes
- Annual recertification records

**Retention:** 3 years past vendor relationship end

---

**Document Revision History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Feb 1, 2026 | Brannon Solomon | Initial vendor management procedure for ISO 42001 |

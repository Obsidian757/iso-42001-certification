# 12th House AI - Data Governance for AI Procedure

**Document Control**
- Version: 1.0
- Effective Date: February 1, 2026
- Owner: Brannon Solomon (Technical Lead)
- Next Review: February 1, 2027

---

## 1. Purpose

This procedure establishes data governance requirements for all AI systems developed, deployed, or managed by 12th House AI, ensuring compliance with:
- ISO/IEC 42001:2023 (Clause 8.3, 8.4)
- NIST AI RMF (Map function)
- OMB M-25-21 (Sec. 5(a)(i) - Data safeguards)
- HIPAA, FERPA, and applicable privacy regulations
- DFARS 252.204-7012 (CUI protection)

---

## 2. Scope

This procedure applies to:
- All data used as input to AI systems
- All data generated or processed by AI systems
- All data stored for AI training, testing, or operation
- Client data processed through VoiceGuard, RMF Navigator, VISTA, or consulting engagements

---

## 3. Data Classification

### 3.1 Data Categories

All data processed by AI systems must be classified into one of these categories:

| Category | Definition | Examples | Handling Requirements |
|----------|------------|----------|----------------------|
| **Public** | Freely distributable, no restrictions | Published blog content, marketing materials | Standard controls |
| **Internal** | Business use only, not externally shared | Internal frameworks, methodologies | Access controls required |
| **Confidential** | Sensitive business or client data | Client project details, pricing, proposals | Encryption + access controls |
| **Regulated** | Subject to legal/regulatory requirements | PII, PHI, CUI, FERPA data | Full compliance controls (see Section 5) |
| **Prohibited** | Never input to AI systems | Classified data, SSNs, payment card data | DO NOT PROCESS with AI |

### 3.2 Classification Responsibility

- **Data Owner:** Person or organization that originates the data
- **12th House AI:** Responsible for applying appropriate controls based on classification
- **Default:** If classification is unknown, treat as **Confidential** until clarified

---

## 4. Data Collection for AI

### 4.1 Data Minimization Principle

Only collect data that is:
- Necessary for the AI system's defined purpose
- Relevant to the specific use case
- Adequate to achieve desired outcomes

**Prohibited:** Collecting data "just in case" or for undefined future use.

### 4.2 Data Source Documentation

For each AI system, document:
- What data sources are used
- How data is collected (API, upload, voice, etc.)
- Who provides the data (client, users, public sources)
- Data format and volume
- Any known limitations or biases in source data

### 4.3 Consent and Authorization

**For PII/PHI:**
- Obtain explicit consent before collecting personal data for AI processing
- Document consent mechanism (terms of service, signed agreement, recorded verbal)
- Honor opt-out requests within 30 days

**For Client Data:**
- Data processing authorization must be in client agreement
- Specify what data may be used for AI purposes
- Clarify data ownership and return/deletion provisions

**For Voice Data (VoiceGuard):**
- Notify users: "This call may be recorded for quality and training purposes"
- Provide opt-out mechanism where feasible
- Do not train AI models on customer voice data without explicit consent

---

## 5. Regulated Data Requirements

### 5.1 Personally Identifiable Information (PII)

**Covered data:** Names, addresses, phone numbers, email addresses, government IDs, biometric data, IP addresses

**Controls:**
- Encrypt at rest and in transit (AES-256 minimum)
- Access limited to authorized personnel only
- Retention limited to business need (default: 90 days)
- De-identify or anonymize before using for AI training
- Right to access, correct, and delete honored within 30 days

### 5.2 Protected Health Information (PHI) - HIPAA

**Covered data:** Medical records, diagnoses, treatment information, health insurance details, any data tied to healthcare

**Additional Controls:**
- Business Associate Agreement (BAA) required with all third-party AI vendors
- Minimum necessary standard: Only access PHI required for specific task
- Audit logging of all PHI access
- Encryption with HIPAA-compliant key management
- 6-year retention of audit logs
- Breach notification within 60 days for affecting 500+ individuals

**VoiceGuard in Healthcare:**
- Must have BAA with ElevenLabs and Vapi (or exclude from PHI use cases)
- Voice recordings containing PHI encrypted and auto-deleted after 30 days
- Do not use healthcare voice data for model training

### 5.3 Controlled Unclassified Information (CUI) - DFARS

**Covered data:** Federal contract information, controlled technical information, export-controlled data, personally identifiable information in federal context

**Controls per NIST 800-171:**
- Access control: Only authorized, cleared personnel
- Awareness and training: Annual CUI handling training
- Audit and accountability: Full logging of CUI access
- Identification and authentication: Multi-factor authentication required
- Incident response: 72-hour breach notification to DoD
- Media protection: Encryption for all storage and transmission
- System protection: FedRAMP or IL5 environments only

**VoiceGuard with CUI:**
- Do NOT process CUI through standard VoiceGuard instance
- Requires Azure GovCloud (IL5) deployment
- Third-party AI (ElevenLabs, Vapi) NOT approved for CUI without explicit authorization

### 5.4 FERPA (Education Data)

**Covered data:** Student education records, grades, attendance, personally identifiable information from education records

**Controls:**
- Protection equivalent to PII
- Consent required from students (18+) or parents (under 18)
- Disclosure only for legitimate educational purpose
- Annual notification to students of FERPA rights

---

## 6. Data Quality for AI

### 6.1 Quality Standards

AI input data must meet these quality criteria:

| Criterion | Definition | Verification Method |
|-----------|------------|---------------------|
| **Accuracy** | Data correctly represents what it claims to measure | Validation against source, sampling checks |
| **Completeness** | No critical missing values | Missing value analysis, null checks |
| **Consistency** | Data matches across sources | Cross-source validation |
| **Timeliness** | Data is current enough for intended use | Date stamp review, staleness checks |
| **Representativeness** | Data reflects target population | Demographic analysis, bias assessment |
| **Validity** | Data conforms to expected format and ranges | Schema validation, range checks |

### 6.2 Data Quality Assessment

Before using data in AI systems:
1. Document data source and collection method
2. Assess against quality criteria above
3. Identify and document any known issues or limitations
4. Determine if data is suitable for intended AI use
5. Implement mitigation for any quality gaps

### 6.3 Data Drift Monitoring

For production AI systems:
- Monitor for data drift (changes in input data patterns over time)
- Alert if data characteristics deviate from training baseline
- Re-assess data quality quarterly or after significant changes
- Retrain AI models if drift impacts performance

---

## 7. Data Processing for AI

### 7.1 Authorized Processing Environments

**Approved environments for AI data processing:**

| Environment | Data Classifications Allowed | Notes |
|-------------|------------------------------|-------|
| Local development machine | Public, Internal | No client or regulated data |
| Claude (Anthropic - Business) | Public, Internal, Confidential | Enterprise DPA required |
| ElevenLabs (Business) | Public, Internal, Confidential | Enterprise DPA required |
| Vapi (Business) | Public, Internal, Confidential | DPA required |
| Azure AI (Commercial) | Public, Internal, Confidential | Commercial cloud |
| Azure GovCloud (IL5) | All except Classified | FedRAMP High, DoD CC SRG IL5 |
| OpenRouter | Public only | No sensitive data |

**Prohibited environments:**
- Free-tier AI services (ChatGPT free, Claude free, etc.) for any client or sensitive data
- Personal devices for regulated data
- Non-U.S. data centers for CUI

### 7.2 Data Transformation

When processing data for AI:
- **De-identification:** Remove direct identifiers (names, SSNs, etc.) before training
- **Anonymization:** Ensure individuals cannot be re-identified from processed data
- **Aggregation:** Combine individual records into summary statistics where possible
- **Tokenization:** Replace sensitive values with tokens for processing, restore if needed

### 7.3 Third-Party Data Processing

For third-party AI vendors processing data:
- Data Processing Agreement (DPA) required
- Vendor must meet SOC 2 or equivalent security standard
- Data localization requirements honored (U.S. only for CUI)
- "Do not train on customer data" provisions in all contracts
- Periodic review of vendor data handling practices

---

## 8. Data Storage and Retention

### 8.1 Storage Requirements

| Data Classification | Storage Location | Encryption Required | Access Control |
|---------------------|------------------|---------------------|----------------|
| Public | Any | Recommended | Basic |
| Internal | Business systems | Required | Role-based |
| Confidential | Encrypted cloud/local | Required (AES-256) | Role-based + logging |
| Regulated | Compliant environment | Required (AES-256) | MFA + logging + audit |

### 8.2 Retention Periods

Default retention periods unless overridden by regulation or contract:

| Data Type | Retention Period | Deletion Trigger |
|-----------|------------------|------------------|
| Active AI system data | Duration of operation | System decommissioning |
| Voice recordings (VoiceGuard) | 30 days | Automatic deletion |
| AI training datasets | 3 years post-model creation | Model retirement |
| Audit logs | 6 years | Regulatory minimum |
| Client engagement data | Duration of contract + 3 years | Project close + retention |
| Incident investigation data | 7 years | Regulatory minimum |

### 8.3 Data Deletion

When data reaches end of retention:
1. Verify no legal hold or regulatory requirement to retain
2. Secure deletion (overwrite, not just delete pointer)
3. Verify deletion from all copies (backups, archives, third-party)
4. Document deletion in data inventory
5. For vendors: Request and retain deletion certificate

---

## 9. Data Access Control

### 9.1 Access Principles

- **Least Privilege:** Grant minimum access necessary for assigned duties
- **Need to Know:** Access based on legitimate business need
- **Separation of Duties:** Prevent single-person control of sensitive operations
- **Default Deny:** No access unless explicitly granted

### 9.2 Access Control Implementation

| Role | Public | Internal | Confidential | Regulated |
|------|--------|----------|--------------|-----------|
| Leadership (Brannon) | ✓ | ✓ | ✓ | ✓ |
| Technical Staff | ✓ | ✓ | ✓ (project-specific) | ✓ (cleared + project) |
| Contractors | ✓ | ✓ (project) | ✓ (signed NDA) | ✗ (unless cleared) |
| Clients | ✓ (their data) | N/A | ✓ (their data only) | ✓ (their data only) |
| Public/Third Party | ✓ | ✗ | ✗ | ✗ |

### 9.3 Access Review

- Quarterly review of all access permissions
- Revoke access within 24 hours of role change or termination
- Annual recertification of access to regulated data

---

## 10. Data Incident Response

### 10.1 Data Breach Definition

A data incident occurs when:
- Unauthorized access to protected data
- Unauthorized disclosure of protected data
- Loss of data containing PII, PHI, or CUI
- Unauthorized modification of protected data
- Data is exposed to AI systems inappropriately

### 10.2 Incident Response Steps

1. **Detect:** Identify potential breach via monitoring or report
2. **Contain:** Stop ongoing access, isolate affected systems
3. **Assess:** Determine scope, data affected, individuals impacted
4. **Notify:** Per regulation requirements (see Section 10.3)
5. **Remediate:** Fix root cause, prevent recurrence
6. **Document:** Full incident report archived for 7 years

### 10.3 Notification Requirements

| Data Type | Notification Requirement | Timeline |
|-----------|--------------------------|----------|
| PII (general) | Affected individuals + regulators if required by state | 30-60 days (varies by state) |
| PHI (HIPAA) | HHS, affected individuals, media if 500+ affected | 60 days |
| CUI (DFARS) | DoD contracting officer | 72 hours |
| FERPA | Parents/students, DoE | As soon as practicable |

---

## 11. Documentation and Audit

### 11.1 Data Inventory

Maintain inventory of all data processed by AI systems:
- Data source and category
- Classification level
- Retention period
- AI systems using this data
- Access controls in place
- Last review date

### 11.2 Processing Records

For regulated data, maintain:
- What data was processed
- When processing occurred
- Who authorized processing
- What AI system was used
- Purpose of processing
- Outcome or output

### 11.3 Audit Support

- Retain all data governance records for 6 years minimum
- Make records available for audit upon request
- Conduct annual self-audit of data governance compliance
- Address findings within 30 days

---

## 12. Training and Awareness

All personnel handling AI data must:
- Complete data governance training within 30 days of hire/assignment
- Annual refresher training on data handling requirements
- Acknowledge data handling responsibilities in writing
- Report suspected data incidents immediately

**Training Topics:**
- Data classification and handling requirements
- PII, PHI, CUI identification and protection
- Incident reporting procedures
- Third-party AI data risks
- Privacy by design principles

---

## 13. Enforcement

Violations of this procedure may result in:
- Removal from AI projects
- Contract termination (for contractors)
- Disciplinary action
- Regulatory penalties (passed to responsible party)
- Civil or criminal liability for intentional violations

---

**Document Revision History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Feb 1, 2026 | Brannon Solomon | Initial data governance procedure for ISO 42001 |

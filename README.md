# Azure Cost Allocation & Chargeback Model

## 1. Project Overview

This project implements an Azure cost allocation and chargeback model
for distributing cloud costs across departments.

The model supports:

- Direct cost assignment
- Shared cost allocation
- Allocation rule validation
- Department-level chargeback
- Audit trail generation
- Cost reconciliation
- Interactive dashboard
- Monthly chargeback reporting

---

## 2. Departments

The demonstration environment contains:

- CSE
- AIML
- IT
- Shared Platform

---

## 3. Cost Allocation Model

### Direct Costs

Department-owned resources are assigned directly to their respective
departments.

### Shared Costs

Shared platform costs are distributed using configured allocation
weights.

| Department | Allocation |
|------------|------------|
| CSE        | 50%        |
| AIML       | 30%        |
| IT         | 20%        |
| Total      | 100%       |

---

## 4. Demonstration Cost Dataset

The current implementation uses synthetic demonstration data.

| Department | Direct Cost | Shared Cost | Chargeback |
|------------|-------------|-------------|------------|
| CSE        | ₹400        | ₹300        | ₹700       |
| AIML       | ₹300        | ₹180        | ₹480       |
| IT         | ₹200        | ₹120        | ₹320       |
| **Total**  | **₹900**    | **₹600**    | **₹1,500** |

---

## 5. Architecture

```text
Azure Resources
       ↓
Cost Data
       ↓
Python Allocation Engine
       ↓
Direct + Shared Allocation
       ↓
Department Chargeback
       ↓
Audit Trail
       ↓
Dashboard + Monthly Report
       ↓
Reconciliation

## 6. Project Structure

```text
azure-chargeback/
├── data/
│   ├── cost_data.csv
│   ├── allocation_rules.csv
│   └── allocation_audit.csv
├── src/
│   ├── chargeback_engine.py
│   ├── dashboard.py
│   └── monthly_report.py
├── output/
│   ├── chargeback_report.csv
│   ├── allocation_audit.csv
│   └── monthly_chargeback_report.pdf
├── METHODOLOGY.md
├── README.md
└── requirements.txt
## 7. Running the Chargeback Engine

Run:

python3 src/chargeback_engine.py

Generated files:

output/chargeback_report.csv
output/allocation_audit.csv

## 8. Running the Dashboard

Run:

streamlit run src/dashboard.py

The dashboard displays:

- Total cost
- Direct cost
- Shared cost
- Department chargeback
- Shared-cost allocation
- Audit trail
- Reconciliation status

## 9. Generating the Monthly Report

Run:

python3 src/monthly_report.py

Generated report:

output/monthly_chargeback_report.pdf

## 10. Validation

The allocation engine validates that allocation percentages equal 100%.

Invalid example:

CSE   50%
AIML  30%
IT    30%
Total 110%

The engine rejects this allocation.

Valid example:

CSE   50%
AIML  30%
IT    20%
Total 100%

The engine processes the allocation successfully.

## 11. Reconciliation

The system compares the original cost against the total departmental chargeback.

Demonstration result:

Original Cost       : ₹1,500.00
Chargeback Total    : ₹1,500.00
Variance            : ₹0.00
Reconciliation      : PASS

## 12. Auditability

The audit trail records:

- Shared resource
- Department
- Allocation driver
- Allocation percentage
- Allocated cost

This provides traceability for shared-cost distribution.

## 13. Governance

The allocation methodology should be documented and agreed upon before production chargeback.

Azure resource ownership is represented through tags such as:

- department
- costCenter
- project
- environment
- owner

Changes to allocation percentages should be reviewed and recorded.

## 14. Data Source

The current implementation uses synthetic demonstration cost data because live Azure Cost Analysis usage data was not available during development.

In a production implementation, cost data can be obtained from Azure Cost Management exports or APIs.

## 15. Limitations

The current MVP uses fixed demonstration allocation weights.

The shared-cost percentages are not measured Azure usage.

Production implementation should replace the demonstration dataset with Azure Cost Management export/API data and calculate allocation drivers from actual usage or an approved business driver.

## 16. Future Scope

Potential production enhancements include:

- Azure Cost Management scheduled exports
- Automated cost ingestion
- Azure Functions / automation
- Usage-based allocation drivers
- Power BI integration
- Budget and cost alerts
- Department dispute workflow
- Historical monthly chargeback tracking

## 17. Project Outcome

The MVP demonstrates an end-to-end Azure cost allocation workflow:

Cost Data
   ↓
Classification
   ↓
Allocation
   ↓
Chargeback
   ↓
Audit
   ↓
Reconciliation
   ↓
Dashboard
   ↓
Monthly Report

The demonstration dataset successfully reconciles with:

₹0.00 variance — PASS

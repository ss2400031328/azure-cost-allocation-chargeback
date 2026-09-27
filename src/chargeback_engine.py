import pandas as pd
import os

# ============================================================
# AZURE COST ALLOCATION & CHARGEBACK ENGINE - V3
# ============================================================

# ------------------------------------------------------------
# 1. Load cost data
# ------------------------------------------------------------

costs = pd.read_csv("data/cost_data.csv")

costs["cost_type"] = costs["cost_type"].str.strip().str.upper()
costs["department"] = costs["department"].str.strip()

# ------------------------------------------------------------
# 2. Load allocation rules
# ------------------------------------------------------------

rules = pd.read_csv("data/allocation_rules.csv")

rules["department"] = rules["department"].str.strip()

# ------------------------------------------------------------
# 3. Validate allocation percentages
# ------------------------------------------------------------

allocation_total = rules["allocation_percentage"].sum()

if abs(allocation_total - 1.0) > 0.0001:
    raise ValueError(
        f"Allocation percentages must equal 100%. "
        f"Current total = {allocation_total * 100:.2f}%"
    )

# ------------------------------------------------------------
# 4. Separate Direct and Shared Costs
# ------------------------------------------------------------

direct_costs = costs[
    costs["cost_type"] == "DIRECT"
].copy()

shared_costs = costs[
    costs["cost_type"] == "SHARED"
].copy()

# ------------------------------------------------------------
# 5. Calculate Direct Cost by Department
# ------------------------------------------------------------

department_costs = (
    direct_costs
    .groupby("department")["cost"]
    .sum()
    .reset_index()
    .rename(columns={"cost": "direct_cost"})
)

# ------------------------------------------------------------
# 6. Calculate Total Shared Cost
# ------------------------------------------------------------

total_shared_cost = shared_costs["cost"].sum()

# ------------------------------------------------------------
# 7. Allocate Shared Cost
# ------------------------------------------------------------

rules["shared_allocated"] = (
    rules["allocation_percentage"] * total_shared_cost
)

# ------------------------------------------------------------
# 8. Create Audit Trail
# ------------------------------------------------------------

audit_rows = []

for _, rule in rules.iterrows():

    audit_rows.append({
        "shared_resource": "shared-platform",
        "department": rule["department"],
        "driver": "Usage",
        "percentage": f"{rule['allocation_percentage'] * 100:.0f}%",
        "allocated_cost": round(rule["shared_allocated"], 2)
    })

audit = pd.DataFrame(audit_rows)

# ------------------------------------------------------------
# 9. Merge Direct + Shared Costs
# ------------------------------------------------------------

report = pd.merge(
    department_costs,
    rules,
    on="department",
    how="outer"
)

report["direct_cost"] = report["direct_cost"].fillna(0)
report["shared_allocated"] = report["shared_allocated"].fillna(0)

# ------------------------------------------------------------
# 10. Calculate Final Chargeback
# ------------------------------------------------------------

report["chargeback_total"] = (
    report["direct_cost"] +
    report["shared_allocated"]
)

# ------------------------------------------------------------
# 11. Reconciliation
# ------------------------------------------------------------

original_total = costs["cost"].sum()

chargeback_total = report["chargeback_total"].sum()

variance = original_total - chargeback_total

if abs(variance) < 0.01:
    reconciliation_status = "PASS"
else:
    reconciliation_status = "FAIL"

# ------------------------------------------------------------
# 12. Create Output Directory
# ------------------------------------------------------------

os.makedirs("output", exist_ok=True)

# ------------------------------------------------------------
# 13. Save Chargeback Report
# ------------------------------------------------------------

report[
    [
        "department",
        "direct_cost",
        "allocation_percentage",
        "shared_allocated",
        "chargeback_total"
    ]
].to_csv(
    "output/chargeback_report.csv",
    index=False
)

# ------------------------------------------------------------
# 14. Save Audit Trail
# ------------------------------------------------------------

audit.to_csv(
    "output/allocation_audit.csv",
    index=False
)

# ------------------------------------------------------------
# 15. Display Report
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("AZURE COST ALLOCATION & CHARGEBACK REPORT")
print("=" * 70)

print("\nDepartment Chargeback:\n")

print(
    report[
        [
            "department",
            "direct_cost",
            "allocation_percentage",
            "shared_allocated",
            "chargeback_total"
        ]
    ].to_string(index=False)
)

print("\n" + "-" * 70)

print(f"Original Cost       : ₹{original_total:,.2f}")
print(f"Chargeback Total    : ₹{chargeback_total:,.2f}")
print(f"Variance            : ₹{variance:,.2f}")
print(f"Reconciliation      : {reconciliation_status}")

print("-" * 70)

print("\nAudit Trail:")
print(audit.to_string(index=False))

print("\nReports saved:")
print("output/chargeback_report.csv")
print("output/allocation_audit.csv")


from pathlib import Path
from datetime import date
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, KeepTogether
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch

# Load generated reports
report = pd.read_csv("output/chargeback_report.csv")
audit = pd.read_csv("output/allocation_audit.csv")
costs = pd.read_csv("data/cost_data.csv")

Path("output").mkdir(exist_ok=True)
pdf_path = "output/monthly_chargeback_report.pdf"

# Calculate totals from source and output data
original_total = costs["cost"].sum()
direct_total = report["direct_cost"].sum()
shared_total = report["shared_allocated"].sum()
chargeback_total = report["chargeback_total"].sum()
variance = original_total - chargeback_total
status = "PASS" if abs(variance) < 0.01 else "FAIL"

# PDF setup
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=(595, 842),
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40
)

styles = getSampleStyleSheet()
styles["Title"].alignment = TA_CENTER
story = []

def heading(text):
    story.append(Paragraph(text, styles["Heading2"]))
    story.append(Spacer(1, 10))

def add_table(data, widths=None):
    table = Table(data, colWidths=widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#163B65")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#EDF3F9")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
    ]))
    story.append(table)
    story.append(Spacer(1, 20))

story.append(Paragraph(
    "Azure Cost Allocation &amp; Chargeback",
    styles["Title"]
))
story.append(Spacer(1, 12))

story.append(Paragraph(
    "Monthly Chargeback Report - Demonstration Dataset",
    styles["Heading2"]
))
story.append(Paragraph(
    f"Generated: {date.today():%d %B %Y}",
    styles["Normal"]
))
story.append(Paragraph(
    "Reporting period: Demonstration period (not actual Azure billing)",
    styles["Normal"]
))
story.append(Spacer(1, 20))

heading("1. Cost Summary")
add_table([
    ["Metric", "Amount (INR)"],
    ["Original Cost", f"{original_total:,.2f}"],
    ["Direct Cost", f"{direct_total:,.2f}"],
    ["Shared Cost", f"{shared_total:,.2f}"],
    ["Total Chargeback", f"{chargeback_total:,.2f}"],
])

heading("2. Department Chargeback")
department_rows = [[
    "Department", "Direct", "Shared", "Total"
]]
for _, row in report.iterrows():
    department_rows.append([
        row["department"],
        f"{row['direct_cost']:,.2f}",
        f"{row['shared_allocated']:,.2f}",
        f"{row['chargeback_total']:,.2f}"
    ])
add_table(department_rows)

heading("3. Shared Cost Allocation Audit")
audit_rows = [[
    "Shared Resource", "Department", "Driver",
    "Percentage", "Allocated"
]]
for _, row in audit.iterrows():
    audit_rows.append([
        row["shared_resource"],
        row["department"],
        row["driver"],
        row["percentage"],
        f"{row['allocated_cost']:,.2f}"
    ])
add_table(audit_rows, [120, 85, 85, 95, 100])

heading("4. Reconciliation")
story.append(Paragraph(
    f"Original Cost: INR {original_total:,.2f}<br/>"
    f"Chargeback Total: INR {chargeback_total:,.2f}<br/>"
    f"Variance: INR {variance:,.2f}<br/>"
    f"<b>Status: {status}</b>",
    styles["Normal"]
))
story.append(Spacer(1, 20))

heading("5. Allocation Methodology")
story.append(Paragraph(
    "Direct costs are assigned to their respective departments. "
    "Shared platform costs are distributed according to the "
    "configured allocation percentages: CSE 50%, AIML 30%, "
    "and IT 20%. These are demonstration allocation weights, "
    "not measured Azure usage.",
    styles["Normal"]
))
story.append(Spacer(1, 20))

heading("6. Data Disclaimer")
story.append(Paragraph(
    "This report uses synthetic demonstration cost data. "
    "It does not represent actual Azure billing charges. "
    "In production, source costs can be imported from "
    "Azure Cost Management exports.",
    styles["Normal"]
))

doc.build(story)

print(f"PDF generated: {pdf_path}")


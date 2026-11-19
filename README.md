# ERPNext Subcontracting Job Work & CGST Sec 143 ITC-04 Reconciler

[![Frappe Framework](https://img.shields.io/badge/Frappe-v15.x-blue.svg)](https://frappeframework.com/)
[![GST Compliance](https://img.shields.io/badge/GST-Section%20143%20Job%20Work-gold.svg)]()
[![ITC-04](https://img.shields.io/badge/Form-GSTR%20ITC--04-blue.svg)]()
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 📌 Executive Overview & Real-World Client Problem

Under **Section 143 of the Central Goods and Services Tax (CGST) Act, 2017**:
1. Raw materials or semi-finished goods sent to a job worker under a Delivery Challan must return to the principal manufacturer within **1 year** (or **3 years** for capital goods).
2. **The Deemed Sale Penalty Trap:** If goods do not return within this window, the initial dispatch is legally deemed a taxable outward supply from the date of the original challan, attracting full GST plus retrospective **18% interest penalties**.
3. Principal manufacturers must file quarterly statutory **Form GST ITC-04** detailing goods sent, received, or supplied from job worker premises.

Manufacturing clients running ERPNext struggle to link multiple inward receipts against original job work delivery challans. This Frappe application solves this audit bottleneck.

---

## 🏛️ System Architecture Flow

```mermaid
flowchart TD
    A["Raw Materials Dispatched to Job Worker"] -->|Generate Delivery Challan (Rule 55)| B["Job Work Challan Master"]
    B -->|Start Statutory Clock| C["Section 143 Aging Clock (365 Days)"]
    D["Processed Goods Received Back"] -->|Subcontracting Receipt| E["Challan Settlement Ledger"]
    E -->|Update Balance Quantity| F{"Challan Fully Closed?"}
    F -->|Yes| G["Challan Closed: Statutory Compliance Met"]
    F -->|Partially Received / Pending| H{"Aging > 365 Days?"}
    H -->|No| I["Active Pending Job Work Balance"]
    H -->|Yes (>365 Days Unreturned)| J["DEEMED SUPPLY TAX TRIGGER: Issue Tax Invoice with 18% Interest"]
    G & I & J --> K["Export Form GST ITC-04 Quarterly Return"]
```

---

## 🚀 Key Engineering Capabilities

- **Rule 55 Job Work Challan Ledger:** Tracks materials sent, scrap produced, and finished components returned.
- **Section 143 1-Year / 3-Year Aging Monitor:** Real-time countdown tracking prevents accidental triggering of deemed supply GST liabilities.
- **Automated GSTR ITC-04 Statement:** Exports statutory quarterly returns ready for the GSTN portal.
- **Scrap & Wastage Accounting:** Captures permissible job work manufacturing wastage tolerances.

---

## 📂 Frappe DocType Schema & Data Structure

```text
jobwork_itc04_gst/
├── jobwork_itc04_gst_core/
│   ├── doctype/
│   │   ├── job_work_challan/
│   │   │   ├── job_work_challan.json
│   │   │   ├── job_work_challan.py
│   │   │   └── job_work_challan.js
│   │   └── itc04_quarterly_statement/
│   │       └── itc04_quarterly_statement.json
│   └── workspace/
│       └── jobwork_itc04_gst_workspace/
│           └── jobwork_itc04_gst_workspace.json
```

---

## ⚡ Frappe Hooks & Whitelisted APIs

- **REST Endpoint:** `POST /api/method/jobwork_itc04_gst.api.dispatch_job_work`
- **Whitelisted Method:** `@frappe.whitelist() def audit_sec143_aging(challan_number, as_of_date_str)`
- **Hooks Event:** `on_submit` of `Subcontracting Receipt` matches against open delivery challans.

---

## 🛠️ Installation & Bench Setup

```bash
bench get-app https://github.com/shyampandey1104/erpnext-jobwork-itc04-gst-reconciler
bench --site erp.yourdomain.com install-app jobwork_itc04_gst
bench --site erp.yourdomain.com migrate
python3 -m unittest discover tests
```

---

## 📄 License
MIT License. Built for Engineering, Textile, Chemical, and Automotive Subcontracting Manufacturers.

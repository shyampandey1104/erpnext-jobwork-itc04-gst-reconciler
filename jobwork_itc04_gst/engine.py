"""CGST Section 143 Job Work & GSTR ITC-04 Compliance Engine."""
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Any, Optional

@dataclass
class JobWorkChallanRecord:
    challan_number: str
    job_worker_gstin: str
    challan_date: str
    item_type: str              # INPUTS (1-yr limit) or CAPITAL_GOODS (3-yr limit)
    sent_quantity: float
    received_quantity: float = 0.0
    status: str = "PENDING_AT_JOB_WORKER"

class JobWorkITC04ReconcilerEngine:
    def __init__(self, principal_gstin: str):
        self.principal_gstin = principal_gstin
        self.challans: Dict[str, JobWorkChallanRecord] = {}

    def dispatch_job_work(self, challan: JobWorkChallanRecord) -> Dict[str, Any]:
        self.challans[challan.challan_number] = challan
        return {"challan_number": challan.challan_number, "status": challan.status}

    def receive_job_work_goods(self, challan_number: str, received_qty: float) -> Dict[str, Any]:
        if challan_number not in self.challans:
            raise ValueError(f"Challan {challan_number} not found.")
        c = self.challans[challan_number]
        c.received_quantity += received_qty
        if c.received_quantity >= c.sent_quantity:
            c.status = "FULLY_RECEIVED_CLOSED"
        else:
            c.status = "PARTIALLY_RECEIVED"
        return {"challan_number": challan_number, "status": c.status, "balance": c.sent_quantity - c.received_quantity}

    def audit_sec143_aging(self, challan_number: str, as_of_date_str: str) -> Dict[str, Any]:
        if challan_number not in self.challans:
            raise ValueError(f"Challan {challan_number} not found.")
        c = self.challans[challan_number]
        
        d_challan = datetime.strptime(c.challan_date, "%Y-%m-%d").date()
        d_audit = datetime.strptime(as_of_date_str, "%Y-%m-%d").date()
        days_elapsed = (d_audit - d_challan).days

        max_allowed_days = 365 if c.item_type == "INPUTS" else 1095
        is_deemed_supply = days_elapsed > max_allowed_days and c.status != "FULLY_RECEIVED_CLOSED"

        return {
            "challan_number": challan_number,
            "item_type": c.item_type,
            "days_elapsed": days_elapsed,
            "max_allowed_days": max_allowed_days,
            "deemed_supply_tax_liability_triggered": is_deemed_supply
        }

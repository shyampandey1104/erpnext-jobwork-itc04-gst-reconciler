import unittest
from jobwork_itc04_gst.engine import JobWorkChallanRecord, JobWorkITC04ReconcilerEngine

class TestJobWorkITC04ReconcilerEngine(unittest.TestCase):
    def setUp(self):
        self.engine = JobWorkITC04ReconcilerEngine("07AAAAA1234A1Z5")

    def test_job_work_dispatch_and_receipt(self):
        c = JobWorkChallanRecord(
            challan_number="JW-CHAL-2026-001", job_worker_gstin="07BBBBA9999B1Z0",
            challan_date="2026-01-10", item_type="INPUTS", sent_quantity=100.0
        )
        self.engine.dispatch_job_work(c)
        rec = self.engine.receive_job_work_goods("JW-CHAL-2026-001", 100.0)
        self.assertEqual(rec["status"], "FULLY_RECEIVED_CLOSED")

    def test_sec143_deemed_sale_breach(self):
        c = JobWorkChallanRecord(
            challan_number="JW-CHAL-2024-999", job_worker_gstin="07BBBBA9999B1Z0",
            challan_date="2024-01-10", item_type="INPUTS", sent_quantity=100.0
        )
        self.engine.dispatch_job_work(c)
        audit = self.engine.audit_sec143_aging("JW-CHAL-2024-999", "2026-03-01")
        self.assertTrue(audit["deemed_supply_tax_liability_triggered"])

if __name__ == "__main__":
    unittest.main()

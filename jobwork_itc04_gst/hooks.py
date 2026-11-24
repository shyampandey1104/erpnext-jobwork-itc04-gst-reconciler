# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "jobwork_itc04_gst"
app_title = "Erpnext Jobwork Itc04 Gst Reconciler"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Jobwork Itc04 Gst Reconciler - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/jobwork_itc04_gst/css/jobwork_itc04_gst.bundle.css"
app_include_js = "/assets/jobwork_itc04_gst/js/jobwork_itc04_gst.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Erpnext Jobwork Itc04 Gst Reconciler Entry": {
        "validate": "jobwork_itc04_gst.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "jobwork_itc04_gst.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "jobwork_itc04_gst.tasks.hourly_sync"
    ],
    "daily": [
        "jobwork_itc04_gst.tasks.daily_reconciliation"
    ],
    "weekly": [
        "jobwork_itc04_gst.tasks.weekly_digest"
    ]
}

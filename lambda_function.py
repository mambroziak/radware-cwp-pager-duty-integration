# https://github.com/PagerDuty/pdpyras

import os
import json
import pdpyras

# declare variables
pd_integration_key = os.environ['pd_integration_key']
pd_event_severity = os.environ['pd_event_severity']
cwp_score_filter = os.environ['cwp_score_filter']
cwp_score_filter = cwp_score_filter.split(',')


def process_alert(msg):
    if msg["score"] in cwp_score_filter:
        payload = {
            "summary": msg["subject"],
            "source": f'{msg["accountVendor"]}:{msg["accountIds"][0]}/{msg["accountName"]}',
            "timestamp": msg["lastDetectionDate"],
            "severity": pd_event_severity,
            "component": msg["resourceType"],
            "group": msg["accountIds"][0],
            "class": msg["category"],
            "custom_details": {
              "failedResources": msg["failedResources"],
              "score": msg["score"],
              "description": msg["description"],
              "recommendation": msg["recommendation"]
            }
        }

        links = [{"href": msg["objectPortalURL"], "text": "Radware CWP Event"}]

        session = pdpyras.EventsAPISession(pd_integration_key)
        dedup_key = session.trigger(summary=None, source=None, links=links, payload=payload)

        if dedup_key:
            success = True
            comments = "Accepted and published to PagerDuty"
        else:
            dedup_key = ""
            success = False
            comments = "Error publishing alert to PagerDuty"

        report = {"success": True, "score": msg["score"], "deduplication_key": dedup_key, "comments": comments}
        return report
    else:
        report = {"success": False, "score": msg["score"], "deduplication_key": "", "comments": "Discarded. Risk score did not meet threshold requirements."}
        return report


def lambda_handler(event, context):
    message = event['Records'][0]['Sns']['Message']
    print("From SNS: " + str(message))
    message = json.loads(message)
    report = process_alert(message)

    print(report)
    return report

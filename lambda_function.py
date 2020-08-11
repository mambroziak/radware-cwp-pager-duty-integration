# https://github.com/PagerDuty/pdpyras
import sys
import time
import random
import string
import os
import json
import pdpyras
pdint_key = "ac6ebbfe53474454a05c1ca1dcc16cfb"

event = {
   "accountIds":[
      "870047315808"
   ],
   "accountName":"SE_Training",
   "accountVendor":"AWS",
   "objectType":"WarningEntity",
   "objectPortalURL":"https://portal.cwp.radwarecloud.com/#/data-center/hardening/332417656708",
   "id":"332417656708",
   "title":"VPC Flow logging is not enabled in some VPCs",
   "score":"4",
   "createdDate":"2020-07-15T15:40:48",
   "vendor":"Radware",
   "apiVersion":"1.00",
   "hardeningType":"Misconfiguration",
   "status":"NEW",
   "category":"misconfigurationResult",
   "resourceType":"VpcEntity",
   "lastDetectionDate":"2020-07-15T15:40:48",
   "description":"VPC Flow Logs is a feature that enables you to capture information about the IP traffic</br> going to and from network interfaces in your VPC. After you've created a flow log, you can</br> view and retrieve its data in Amazon CloudWatch Logs or S3.</br> VPC Flow Logs provide visibility into network traffic that traverses the VPC and can be</br> used to detect anomalous traffic or insight during security workflows.",
   "recommendation":"Enable VPC Flow logs for your VPCs.</br>Refer to this <a href=\"https://docs.aws.amazon.com/vpc/latest/userguide/working-with-flow-logs.html#create-flow-log\">AWS user guide</a> for help",
   "subject":"VPC Flow logging is not enabled in some VPCs in account SE_Training (id:870047315808)",
   "failedResources":[
      {
         "name":"VPC-SETRAINING-US",
         "id":"vpc-05346d1c9dc9bbe82",
         "createdDate":"2020-05-19T23:01:26",
         "passed":"true",
         "region":"us-east-1",
         "link":"https://console.aws.amazon.com/vpc/home?#vpcs:VpcId=VPC_ID"
      },
      {
         "name":"vpc-116c4776",
         "id":"vpc-116c4776",
         "createdDate":"2020-05-19T23:00:56",
         "passed":"false",
         "detectionDate":"2020-08-03T05:43:48",
         "region":"ap-northeast-1",
         "link":"https://console.aws.amazon.com/vpc/home?#vpcs:VpcId=VPC_ID"
      }
   ]
}


def main():
#    api_token = 'K1gn-xJEwr9yC-6iaAJ3'
#    session = pdpyras.APISession(api_token)
#    for user in session.iter_all('users'):
#        print(user['id'], user['email'], user['name'])

    payload = {
        "summary": event["subject"],
        "source": f'{event["accountVendor"]}:{event["accountIds"][0]}/{event["accountName"]}',
        "timestamp": event["lastDetectionDate"],
        "severity": "critical",
        "component": event["resourceType"],
        "group": event["accountIds"][0],
        "class": event["category"],
        "custom_details": {
          "failedResources": event["failedResources"],
          "score": event["score"],
          "description": event["description"],
          "recommendation": event["recommendation"]
        }
    }

    links = [{"href": event["objectPortalURL"], "text": "Radware CWP Event"}]

    session = pdpyras.EventsAPISession(pdint_key)
    dedup_key = session.trigger(summary=None, source=None, links=links, payload=payload)
    print(dedup_key)


# https://events.pagerduty.com/v2/enqueue

def lambda_handler(event, context):
    report = process_messages()
    return {
        'report': report
    }


if __name__ == '__main__': main()

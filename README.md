# Radware CWP Pager Duty Integration
#### _with Events API_

This open source AWS tool consumes the published security findings detected in Radware CWP. This tool passes findings when the CWP risk score is matched in the score filter. Findings not found in the fitler will be discarded. Accepted findings will trigger an event in PagerDuty events API.

<img src="docs/pictures/Radware_CWP_S3_Logger.jpg">

The CFT deployment process will create an SNS Topic, an IAM Role, CloudWatch Log Group (default 30 days retention), and a Lambda Function. Messages published to the created SNS Topic trigger the Lambda Function on-demand.

## Setup

### CFT Parameters
This CFT stack has 5 parameters, 4 of which are configured during deployment:

- **PagerDutyIntegrationKey** -  PagerDuty integration (routing) key
- **PagerDutySeverity** - PagerDuty event severity level for alerts (values: `critical`/`error`/`warning`/`info`)
- **CwpScoreFilter** - CWP risk scores which will trigger a PagerDuty alert (comma separated values: 1 through 10)

### [Option 1] One-click CFT Deployment:
[<img src="docs/pictures/cloudformation-launch-stack.png">](https://console.aws.amazon.com/cloudformation/home?#/stacks/new?stackName=RadwareCWP-PagerDuty-Integration&templateURL=https://radware-cwp-devops-us-east-1.s3.amazonaws.com/radware_cwp_pagerduty_integration/radware_cwp_pagerduty_integration.yaml)
> Note: One-click CFT deployment currently works for regions: us-east-1, us-east-2, us-west-1, us-west-2, ca-central-1, eu-central-1. The AWS region you are actively logged into will be the region of deployment.
1. Fill in the parameter fields. 
1. Click **Next** twice.
1. Under **Capabilities and transforms**, click to check the **3** pending acknowledgements: "_I acknowledge..._".
1. Click **Create stack**.
1. After the process finished view the **Outputs** tab. The **InputTopicARN** value will be needed for the next step in the CWP console.

### [Option 2] Manual CFT Deployment:
1. Download the contents of this repo.
1. Add `lambda_function.py` into the root of a zip file (e.g. `myfunction.zip`).
1. Upload the zip file to an S3 bucket 
1. Modify `radware_cwp_pagerduty_integration.yaml` lines `47` and `52` and enter values for `bucket` and `key` (zip file), respectively. Remove lines `48-51`.
1. Login to the AWS console, select a region, and navigate to CloudFormation. 
1. Click **Create stack**
1. Under **Specify template**, click **Upload a template file**
1. Click the **Choose file** button and upload the modified CFT.
1. Click **Next** twice.
1. Under **Capabilities and transforms**, click to check the **3** pending acknowledgements: "_I acknowledge..._". (or use "--capabilities CAPABILITY_IAM" if using the AWS CLI.)
1. Click **Create stack**.
1. After the process finished view the **Outputs** tab. The **InputTopicARN** value will be needed for the next step in the Radware CWP console.

## Post-Deployment Steps

### Radware CWP Setup:
1. Log into **Radware CWP** and then click **Settings** > **Manage Cloud Accounts** from the menu at the top. 
1. Find the AWS cloud account you want to get alerts from in the list, click **Activate** under the **Automated Response** column.
1. In the **Activate Automated Response** dialogue box, under step 2, paste the **InputTopicARN** value from the CFT deployment process. 
1. Click **Activate**.
All done!

## Build your own deployment file to publish to Lambda
1. Create a new instance with Amazon Linux 
2. Login and validate your are using same version of Python as this Lambda Function runtime (v3.8+).
3. Clone this project `git clone https://github.com/mambroziak/radware-cwp-pager-duty-integration.git`
4. Change into the project root directory `cd radware-cwp-pager-duty-integration`
5. Change to root of the project directory.
6. Run the following code to install the dependencies and build the Lambda deployment zip file.
```
pip install --target ./package pdpyras
# More info: https://github.com/PagerDuty/pdpyras
chmod -R 755 .
cd package
zip -r9 ${OLDPWD}/radware_cwp_pagerduty_integration.zip .
cd $OLDPWD
zip -g radware_cwp_pagerduty_integration.zip lambda_function.py
```
7. Publish the deployment file to lambda.
```
aws lambda update-function-code \
 --function-name <my-function-name> \
 --zip-file fileb://radware_cwp_pagerduty_integration.zip\
 --publish \
 --region=us-east-1
```

## License
This project is licensed under the MIT License

# https://github.com/PagerDuty/pdpyras
# pip install --target ./package pdpyras
# chmod -R 755 .
# cd package
# zip -r9 ${OLDPWD}/function.zip .
# cd $OLDPWD
# zip -g function.zip lambda_function.py
#  aws lambda update-function-code \
#  --function-name RadwareCWP-PagerDuty-Integration \
#  --zip-file fileb://myfunction.zip \
#  --publish \
#  --region=us-east-1
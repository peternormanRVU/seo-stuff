
Section 1: configuration and connect to Google ads API
1. Please ensure you have admin access to your google adwords account. 
2. Login to Google adwords account and get developer token.You can retrieve your developer token by signing in to your manager account then going to the AdWords API Center 
page (Tool icon > SETUP > API Center).
3. Create a client_id and client_secret. For details, please see https://developers.google.com/adwords/api/docs/guides/authentication#installed
4. Generate refresh_token. If you are unable to generate refresh token from the UI, you can run below script
    python refresh_token.py --client_id INSERT_CLIENT_ID --client_secret INSERT_CLIENT_SECRET
5. update your account id, client id, client secret and refresh token in the google-ads.yaml file
6. Update the path in utlities.py to specify the yaml file in your local direcotry. 


Section 2: create a keyword plan in a Google ads account
1. Prepare keywords - put a list of keywords in a CSV file and store in your local file directory. 
2. update the path in utilities.py ReadCSV function: let the program knows where to read the file in your local file directory. 
3. update keyword plan name in main function under CreateKeywordsPlan.py
4. Run the script python CreateKeywordsPlan.py -c client_id to create the keyword plan in Google ads

Section 3. Pull the keyword data from a keyword plan
1. Get the plan_id for the keyword plan (we just created in section 2) from Google ads.
2. Run python get_report.py -c account_id -k plan_id -n file_name.csv

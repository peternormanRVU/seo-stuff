import argparse
import sys
from utilities import Utilities
from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException
import _locale
import pandas as pd


#commond line: python get_report.py -c account_id -k plan_id -n file_name.csv

#account id: 4373090880
#plan-id for insurance: 275899813
#plan-id for credit card: 275652245
#plan-id for loans: 275466159
#plan-id for savings: 275899813
#plan-id for mortgages: 275657588
#plan-id for current accounts: 275658347


_locale._getdefaultlocale = (lambda *args: ['en_UK', 'UTF-8'])

# [START generate_forecast_metrics]
def main(client, customer_id, keyword_plan_id, file_name):
    keyword_plan_service = client.get_service("KeywordPlanService")
    resource_name = keyword_plan_service.keyword_plan_path(customer_id, keyword_plan_id)
    
    try:
        response = keyword_plan_service.generate_historical_metrics(resource_name)
        #response = keyword_plan_service.generate_forecast_metrics(resource_name)
    except GoogleAdsException as ex:
        print(
            'Request with ID "{}" failed with status "%s" and includes the "following errors:"'.format(ex.request_id, ex.error.code().name)
        )
        for error in ex.failure.errors:
            print('\tError with message "{}".'.format(error.message))
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(
                        "\t\tOn field: {}".format(field_path_element.field_name)
                    )
        sys.exit(1)

    keywordCollection = []

    for i, forecast in enumerate(response.metrics):
        keyword = forecast.search_query
        metrics = forecast.keyword_metrics
        competition = metrics.competition
        kw_sv_monthly_pair =[]
        kw_sv_monthly_pair.append(keyword)
        kw_sv_monthly_pair.append(str(competition))
        
        sv_by_month = metrics.monthly_search_volumes
        for element in sv_by_month:
            kw_sv_monthly_pair =[]
            kw_sv_monthly_pair.append(keyword)
            kw_sv_monthly_pair.append(str(competition))
            sv_volume = element.monthly_searches
            sv_month = str(element.year) + "-" + str(element.month-1)
            kw_sv_monthly_pair.append(sv_month)
            kw_sv_monthly_pair.append(sv_volume)
            keywordCollection.append(kw_sv_monthly_pair)

        #keywordCollection.append(kw_sv_monthly_pair)
    
    frame = pd.DataFrame(keywordCollection, columns = ['keyword', 'competition level', 'month', 'search volume'])
    frame.to_csv('C:\\python-project\\keyword-planner-api\\{}'.format(file_name), index=False, encoding='utf-8')

        

if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    utilityObject = Utilities()
    google_ads_client = utilityObject.CreateAPIClient()

    parser = argparse.ArgumentParser(
        description="Generates forecast metrics for a keyword plan."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    parser.add_argument(
        "-k",
        "--keyword_plan_id",
        type=str,
        required=True,
        help="A Keyword Plan ID.",
    )
    parser.add_argument(
        "-n",
        "--file_name",
        type=str,
        required=True,
        help="export file name.",
    )
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.keyword_plan_id, args.file_name)
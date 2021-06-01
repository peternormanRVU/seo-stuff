#!/usr/bin/env python
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This example creates a keyword plan.
Keyword plans can be reused for retrieving forecast metrics and historic
metrics.
"""


import argparse
import sys
import uuid
from utilities import Utilities
from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException
import _locale

_locale._getdefaultlocale = (lambda *args: ['en_UK', 'UTF-8'])

# [START add_keyword_plan]
def main(client, customer_id):
    """Adds a keyword plan, campaign, ad group, etc. to the customer account
    Also handles errors from the API and prints them.
    Args:
        client: An initialized instance of GoogleAdsClient
        customer_id: A str of the customer_id to use in requests.
    """
    try:
        plan_name = "energy-sheet-3"
        add_keyword_plan(client, customer_id, plan_name)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)


def add_keyword_plan(client, customer_id, plan_name):
    """Adds a keyword plan, campaign, ad group, etc. to the customer account.
    Args:
        client: An initialized instance of GoogleAdsClient
        customer_id: A str of the customer_id to use in requests.
    Raises:
        GoogleAdsException: If an error is returned from the API.
    """
    keyword_plan = create_keyword_plan(client, customer_id, plan_name)
    keyword_plan_campaign = create_keyword_plan_campaign(
        client, customer_id, keyword_plan
    )
    keyword_plan_ad_group = create_keyword_plan_ad_group(
        client, customer_id, keyword_plan_campaign
    )
    create_keyword_plan_ad_group_keywords(
        client, customer_id, keyword_plan_ad_group
    )



def create_keyword_plan(client, customer_id, plan_name):
    """Adds a keyword plan to the given customer account.
    Args:
        client: An initialized instance of GoogleAdsClient
        customer_id: A str of the customer_id to use in requests.
    Returns:
        A str of the resource_name for the newly created keyword plan.
    Raises:
        GoogleAdsException: If an error is returned from the API.
    """
    operation = client.get_type("KeywordPlanOperation", version="v6")
    keyword_plan = operation.create

    keyword_plan.name = f"Keyword plan for {plan_name}"

    forecast_interval = client.get_type(
        "KeywordPlanForecastIntervalEnum", version="v6"
    ).NEXT_QUARTER
    keyword_plan.forecast_period.date_interval = forecast_interval

    keyword_plan_service = client.get_service(
        "KeywordPlanService", version="v6"
    )
    response = keyword_plan_service.mutate_keyword_plans(
        customer_id, [operation]
    )
    resource_name = response.results[0].resource_name

    print(f"Created keyword plan with resource name: {resource_name}")

    return resource_name


def create_keyword_plan_campaign(client, customer_id, keyword_plan):
    """Adds a keyword plan campaign to the given keyword plan.
    Args:
        client: An initialized instance of GoogleAdsClient
        customer_id: A str of the customer_id to use in requests.
        keyword_plan: A str of the keyword plan resource_name this keyword plan
            campaign should be attributed to.create_keyword_plan.
    Returns:
        A str of the resource_name for the newly created keyword plan campaign.
    Raises:
        GoogleAdsException: If an error is returned from the API.
    """
    operation = client.get_type("KeywordPlanCampaignOperation", version="v6")
    keyword_plan_campaign = operation.create

    keyword_plan_campaign.name = f"Keyword plan campaign {uuid.uuid4()}"
    keyword_plan_campaign.cpc_bid_micros = 1000000
    keyword_plan_campaign.keyword_plan = keyword_plan

    keyword_plan_network = client.get_type(
        "KeywordPlanNetworkEnum", version="v6"
    )
    network = keyword_plan_network.GOOGLE_SEARCH
    keyword_plan_campaign.keyword_plan_network = network

    geo_target = client.get_type("KeywordPlanGeoTarget", version="v6")
    # Constant for U.S. Other geo target constants can be referenced here:
    # https://developers.google.com/adwords/api/docs/appendix/geotargeting
    # 2840 - US, 20339 - GB
    geo_target.geo_target_constant = "geoTargetConstants/20339"
    keyword_plan_campaign.geo_targets.append(geo_target)

    keyword_plan_campaign.language_constants.append("languageConstants/1000")

    keyword_plan_campaign_service = client.get_service(
        "KeywordPlanCampaignService", version="v6"
    )
    response = keyword_plan_campaign_service.mutate_keyword_plan_campaigns(
        customer_id, [operation]
    )

    resource_name = response.results[0].resource_name

    print(f"Created keyword plan campaign with resource name: {resource_name}")

    return resource_name


def create_keyword_plan_ad_group(client, customer_id, keyword_plan_campaign):
    """Adds a keyword plan ad group to the given keyword plan campaign.
    Args:
        client: An initialized instance of GoogleAdsClient
        customer_id: A str of the customer_id to use in requests.
        keyword_plan_campaign: A str of the keyword plan campaign resource_name
            this keyword plan ad group should be attributed to.
    Returns:
        A str of the resource_name for the newly created keyword plan ad group.
    Raises:
        GoogleAdsException: If an error is returned from the API.
    """
    operation = client.get_type("KeywordPlanAdGroupOperation", version="v6")
    keyword_plan_ad_group = operation.create

    keyword_plan_ad_group.name = f"Keyword plan ad group {uuid.uuid4()}"
    keyword_plan_ad_group.cpc_bid_micros = 2500000
    keyword_plan_ad_group.keyword_plan_campaign = keyword_plan_campaign

    keyword_plan_ad_group_service = client.get_service(
        "KeywordPlanAdGroupService", version="v6"
    )
    response = keyword_plan_ad_group_service.mutate_keyword_plan_ad_groups(
        customer_id, [operation]
    )

    resource_name = response.results[0].resource_name

    print(f"Created keyword plan ad group with resource name: {resource_name}")

    return resource_name


def create_keyword_plan_ad_group_keywords(client, customer_id, plan_ad_group):
    """Adds keyword plan ad group keywords to the given keyword plan ad group.
    Args:
        client: An initialized instance of GoogleAdsClient
        customer_id: A str of the customer_id to use in requests.
        keyword_plan_ad_group: A str of the keyword plan ad group resource_name
            these keyword plan keywords should be attributed to.
    Raises:
        GoogleAdsException: If an error is returned from the API.
    """
    match_types = client.get_type("KeywordMatchTypeEnum", version="v6")

    utility = Utilities()
    data = utility.ReadCSV()
    if len(data) != 0:
        keywordsCollection = []
        for keyword in data:
            keyword_plan_ad_group_keyword = client.get_type("KeywordPlanAdGroupKeyword", version="v6")
            keyword_plan_ad_group_keyword.text = keyword
            keyword_plan_ad_group_keyword.cpc_bid_micros = 1990000
            keyword_plan_ad_group_keyword.match_type = match_types.EXACT
            keyword_plan_ad_group_keyword.keyword_plan_ad_group = plan_ad_group
            keywordsCollection.append(keyword_plan_ad_group_keyword)


    operations = []
    for keyword in keywordsCollection:
        operation = client.get_type(
            "KeywordPlanAdGroupKeywordOperation", version="v6"
        )
        operation.create.CopyFrom(keyword)
        operations.append(operation)

    keyword_plan_ad_group_keyword_service = client.get_service(
        "KeywordPlanAdGroupKeywordService", version="v6"
    )

    response = keyword_plan_ad_group_keyword_service.mutate_keyword_plan_ad_group_keywords(
        customer_id, operations
    )

    for result in response.results:
        print(
            "Created keyword plan ad group keyword with resource name: "
            f"{result.resource_name}"
        )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    utilityObject = Utilities()
    google_ads_client = utilityObject.CreateAPIClient()

    parser = argparse.ArgumentParser(
        description="Creates a keyword plan for specified customer."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    args = parser.parse_args()

    #main(google_ads_client, args.customer_id)
    main(6182214629, 9484003108)
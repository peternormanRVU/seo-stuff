import csv
import google.ads.google_ads.client
import pandas as pd
from googleads import adwords
import os

class Utilities:

    #path = "C:\\python-project\\keyword-planner-api\\google-ads.yaml"
    path = "C:\\Users\\PeterNorman\\PycharmProjects\\keyword-planner-api\\google-ads.yaml"

    # def ReadFiles(self):
    #     folderPath = "C:\\python-project\\keyword-planner-api\\kw-folder"
    #     for root, dirs, files in os.walk(folderPath):
    #         for file in files:
    #             with open(os.path.join(root, file), newline='') as f:


    def ReadCSV(self):
        path = "C:\\Users\\PeterNorman\\PycharmProjects\\keyword-planner-api\\energy-sheet-3.csv"
        with open(path, newline='') as f:
            data = []
            reader = csv.reader(f)
            for row in reader:
                data.append(row[0])
        return data

    def CreateAPIClient(self):
        path = "C:\\Users\\PeterNorman\\PycharmProjects\\keyword-planner-api\\google-ads.yaml"
        google_ads_client = (
            google.ads.google_ads.client.GoogleAdsClient.load_from_storage(path)
        )
        return google_ads_client

    def CreateAdWordClient(self):
        path = "C:\\Users\\PeterNorman\\PycharmProjects\\keyword-planner-api\\google-ads.yaml"
        adwords_client = adwords.AdWordsClient.LoadFromStorage(path)
        return adwords_client

    def GetSearchVolume(self, google_ads_client, keywordsCollection):
        frame = pd.DataFrame()
        
        targetService = google_ads_client.GetService('TargetingIdeaService')
        sublists = [keywordsCollection[x:x+10] for x in range(0,len(keywordsCollection),10)]

        count = 0
        kw_sv_list = []
        for sublist in sublists:
            if (count ==10):
                frame = pd.DataFrame(kw_sv_list, columns = ['keyword', 'search volume'])
                frame.to_csv('C:\\python-project\\keyword-planner-api\\result.csv', index=False, encoding='utf-8')
                print(frame)
                exit()
            selector = {
                'ideaType': 'KEYWORD',
                'requestType': 'STATS'
            }

            selector['requestedAttributeTypes'] = [
                    'KEYWORD_TEXT',
                    'SEARCH_VOLUME'
            ]

            offset = 0
            selector['paging'] = {
                  'startIndex' : str(offset),
                  'numberResults' : str(len(sublist))
            }

            selector['searchParameters'] = [{
                  'xsi_type' : 'RelatedToQuerySearchParameter',
                  'queries' : sublist
            }]

            # Language setting (optional).
            selector['searchParameters'].append({
                'xsi_type': 'LanguageSearchParameter',
                'languages': [{'id': '1000'}]
            })

            # Network search parameter (optional) - only for Google search
            selector['searchParameters'].append({
                'xsi_type': 'NetworkSearchParameter',
                'networkSetting': {
                    'targetGoogleSearch': True,
                    'targetSearchNetwork': False,
                    'targetContentNetwork': False,
                    'targetPartnerSearchNetwork': False
                }
            })

            try: 
                page = targetService.get(selector)
            except:
                return frame

            if 'entries' in page:
                for i in range(0, len(page['entries'])):
                    kw_sv_pair = list()
                    kw_sv_pair.append(page['entries'][i]['data'][0]['value']['value'])
                    kw_sv_pair.append(page['entries'][i]['data'][1]['value']['value'])
                    kw_sv_list.append(kw_sv_pair)

            count = count +1
        frame = pd.DataFrame(kw_sv_list, columns = ['keyword', 'search volume'])
        frame.to_csv('C:\python-project\keyword-planner-api\result.csv', index=False, encoding='utf-8')
        return frame


# obj = Utilities()
# obj.ReadFiles()
        

















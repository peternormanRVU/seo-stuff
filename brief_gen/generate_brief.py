from selenium import webdriver
from bs4 import BeautifulSoup
import re
import datetime
import time
import pandas as pd
import glob, os
from distutils.dir_util import copy_tree
from pathlib import Path
from PIL import Image


class Brief_data(object):

    def __init__(self,urls, topic, keyword):
        self.topic = topic
        self.keyword = keyword
        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        #self.options.add_argument("--window-size=800,800")
        # self.browser = webdriver.Chrome(executable_path='chromedriver', options=self.options)  #Windows works with simpler path option
        self.browser = webdriver.Chrome(executable_path='C:/Users/PeterNorman/PycharmProjects/brief_gen', options=self.options)  #Add path to your Chromedriver
        self.url_queue = urls #Add the start URL to our list of URLs to crawl
        self.output_file = f"briefs/{topic}"
        self.sleep = 1
        self.data = {}


    def get_page(self, url, position):
        try:
            self.browser.get(url)
            S = lambda X: self.browser.execute_script('return document.body.parentNode.scroll' + X)
            self.browser.set_window_size('1000', S('Height'))  # May need manual adjustment
            self.browser.find_element_by_tag_name('body')
            filename = "{}/screenshots/{}.png".format(self.output_file,position)
            self.browser.save_screenshot(filename)
            return self.browser.page_source, filename
        except Exception as e:
            print(e)
            return

    def get_soup(self, html):
        if html is not None:
            soup = BeautifulSoup(html, 'html.parser')
            return soup
        else:
            return None

    def page_summary(self, soup, body_content):

        # Images
        find_body = soup.find('body')
        images = len(find_body.find_all('img'))

        # Word count
        words = len(body_content.split(" "))

        # soup = BeautifulSoup(soup,'html.parser')

        # Schema

        #TODO

        # Title

        title = soup.title
        if title :
            title = title.text


        # Heading 1

        h1 = soup.find('h1')
        if h1:
            h1 = h1.text


        # Heading 2

        h2 =  soup.find_all('h2')
        if h2:
            h2 = [item.text for item in h2]
            h2_len = len(h2)
        else:
            h2 = None
            h2_len = 0


        # Heading 3

        h3 = soup.find_all('h3')
        if h3:
            h3 = [item.text for item in h3]
            h3_len = len(h3)
        else:
            h3 = None
            h3_len = 0

        # Meta description

        description = soup.find("meta", property="description")
        if description:
            description = description.text

        data = {'description': description,'title':title,'h1':h1,'h2':h2,'h3':h3,'words':words,'images':images, 'len-h2':h2_len,'len-h3':h3_len}
        return data

    def get_data(self,soup):
        try:
            whitelist = ['title','h1','h2','h3','h4','h5','p','li']
            body = soup.find('body')
            keep = []

            for tag in body.findAll(True):
                if tag.name not in whitelist:
                    tag.hidden = True

            body_content = " ".join([t for t in soup.find_all(text=True) if t.parent.name in whitelist])

            data = self.page_summary(soup, body_content)

            # return str(soup.renderContents())
            return re.sub("(<|</)body.*>",'',str(body_content)), data
        except Exception as e:
            print(e)

        return 1

    def run_crawler(self):

        for i in self.url_queue: #If we have keywords to check
            url, position = i #We grab a keyword from the left of the list
            html, screenshot_location = self.get_page(url, position)
            soup= self.get_soup(html)
            time.sleep(self.sleep) # Wait for the specified time
            if soup is not None:  #If we have soup - parse and save data
                self.data[position], data = self.get_data(soup)
                self.data['url-{}'.format(position)] = url
                self.data['data-{}'.format(position)] = data
            print(f'Grabbed - {url}')

        # Generate serp summary by going through the data keys
        #TODO
        # self.summary = {'images'}
        # for key, value in self.data.items():
        #     key.contains('data'):



        self.browser.quit()

class generate_html(object):
    def __init__(self, topic, keyword, data, table, comment):
        self.directory = f"briefs/{topic}"
        self.topic = topic
        self.keyword = keyword
        self.data = data
        self.soup = BeautifulSoup(open(f"{str(os.getcwd())}/briefs/{topic}/index.html"), "html.parser")
        table = table.loc[:, table.columns.isin(['Keyword', 'Volume','Include in heading'])]
        self.table = self.gen_table(table)
        self.comment = comment
        self.update_html()
        self.save()
        self.resize_screenshots()

    def resize_screenshots(self):
        # Images from the selenium driver are random sizes need to resize all to
        basewidth = 1000
        for file in os.listdir(f"{str(os.getcwd())}/briefs/{self.topic}/screenshots"):
            img = Image.open(f"{str(os.getcwd())}/briefs/{self.topic}/screenshots/{file}")
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            img.save(f"{str(os.getcwd())}/briefs/{self.topic}/screenshots/{file}")


    def gen_table(self, table):
        headings = ['Keyword', 'Volume','Include in heading']

        new_table = self.soup.new_tag('table', id='example')
        new_table['class'] = "display"
        new_table['style'] = "width:100%"
        head = self.soup.new_tag('thead')
        tr = self.soup.new_tag('tr')
        for row in headings:
            th = self.soup.new_tag('th')
            tr.append(th)
            th.append(str(row))
            tr.append(th)
        head.append(tr)
        new_table.append(head)


        body = self.soup.new_tag('tbody')

        for row in table.values.tolist():
            tr = self.soup.new_tag('tr')
            for attr in row:
                th = self.soup.new_tag('th')
                tr.append(th)
                if str(attr) == 'nan':
                    th.append("")
                else:
                    th.append(str(attr))
                tr.append(th)
            body.append(tr)
        new_table.append(body)
        return new_table

    def save(self):
        with open(f"{str(os.getcwd())}/briefs/{self.topic}/index.html", "w") as file:
            file.write(str(self.soup))

    def update_html(self):
        # Update the topic & info fields
        topic = self.soup.find_all('span', attrs={'id':'primary-topic'})
        if topic:
            for i in topic:
                i.string = self.topic
        #
        # Update the keyword & generated date
        keyword = self.soup.find_all('span', attrs={'id': 'primary-keyword'})
        if keyword:
            for i in keyword:
                i.string = self.keyword

        date = self.soup.find('span', attrs={'id': 'date-gen'})
        if date:
            date.string = str(datetime.datetime.today())

        # SEO comment

        comment = self.soup.find('p', attrs={'id': 'seo-comment'})
        if comment:
            comment.string = self.comment

        # And the table
        table = self.soup.find('table', attrs={'id': 'example'})
        if table:
            table = table.replace_with(self.table)

        # Update content
        for i in range(1,10):
            try:
                # Update the content
                cont = self.soup.find('span', attrs={'id': f"content-{i}"})
                cont.string = self.data[i].replace('\n\n',"")
                cont.string = re.sub("""\n \n""",'',cont.string)
                # Update the url
                url = self .soup.find('span', attrs={'id': f"link-{i}"})
                url.string = self.data[f"url-{i}"]
                content_elements = ['title','description','h1','h2','h3','words','images','len-h2','len-h3']
                for elem in content_elements:
                    try:
                        if elem in ['title','description','images','words','h1','len-h2','len-h3']:
                            item = self.soup.find('span', attrs={'id': f"{elem}-{i}"})
                            item.string = str(self.data[f"data-{i}"][f"{elem}"])
                        # Create unordered lists for multiple results 
                        else:
                            # Create unorder list tag with
                            new_list = self.soup.new_tag('ul')
                            for a in self.data[f"data-{i}"][f"{elem}"]:
                                li = self.soup.new_tag('li')
                                li.append(a)
                                new_list.append(li)
                            item = self.soup.find('span', attrs={'id': f"{elem}-{i}"})
                            if item:
                                item.append(new_list)
                    except Exception as e:
                        print(e)
                # update the stats
            except Exception as e:
                print(e)
                break

if __name__ == "__main__":
    # Read the brief excel template
    df = pd.read_excel('template.xlsx', sheet_name='summary')
    df_keywords = pd.read_excel('template.xlsx', sheet_name='keywords')
    df_urls = pd.read_excel('template.xlsx', sheet_name='urls')

    # Loop through the summary sheet and create the briefs

    for brief in df.values.tolist():
        urls = df_urls[df_urls['page'] == brief[0]]
        u = [x for x in urls[['urls','position']].values.tolist() if str(x[0]) != 'nan']
        keyword_table = df_keywords[df_keywords['Page'] == brief[0]]

        # Copy the home template folder in the outputs folder
        try:
            os.mkdir(f"briefs/{brief[0]}")
            fromDirectory = "home"
            toDirectory = f"briefs/{brief[0]}"
            copy_tree(fromDirectory, toDirectory)
            os.chdir(f"briefs/{brief[0]}")
            os.chdir(Path(os.getcwd()).parent.parent)
        except:
            pass

        # Return the data and save the screenshots for the brief

        ranker = Brief_data(u, brief[0], brief[1])  # urls, topic, keyword
        ranker.run_crawler() # Run the rank checker

        # Send the returned data to update the brief template

        a = generate_html(brief[0], brief[1], ranker.data, keyword_table, brief[2]) # Topic, keyword, data, table, comment
        a.update_html()

        print(brief[0] + " updated")



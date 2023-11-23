

import urllib.request, sys, time
from bs4 import BeautifulSoup
import requests
import pandas as pd

pagesToGet = 5

all_data = []  # Create an empty list to store all the data

for page in range(1, pagesToGet + 1):
    print('processing page:', page)
    url = 'https://www.newsinlevels.com/' + str(page)
    print(url)

    # an exception might be thrown, so the code should be in a try-except block
    try:
        # use the browser to get the url. This is a suspicious command that might blow up.
        page = requests.get(url)  # this might throw an exception if something goes wrong.

    except Exception as e:  # this describes what to do if an exception is thrown
        error_type, error_obj, error_info = sys.exc_info()  # get the exception information
        print('ERROR FOR LINK:', url)  # print the link that caused the problem
        print(error_type, 'Line:', error_info.tb_lineno)  # print error info and line that threw the exception
        continue  # ignore this page. Abandon this and go back.

    time.sleep(2)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('li', attrs={'class': 'o-listicle__item'})
    print(len(links))

    for j in links:
        link = "https://www.newsinlevels.com/"
        link += j.find("div", attrs={'class': 'm-statement__quote'}).find('a')['href'].strip()

        # Now, extract data from the inner link
        inner_page = requests.get(link)
        inner_soup = BeautifulSoup(inner_page.text, 'html.parser')

        statement = inner_soup.find("div", attrs={'class': 'm-statement__quote'}).text.strip()
        
        # Check if the 'footer' element exists before accessing its 'text' attribute
        date_element = inner_soup.find('div', attrs={'class': 'm-statement__body'}).find('footer')
        date = date_element.text[-14:-1].strip() if date_element else 'N/A'
        
        source = inner_soup.find('div', attrs={'class': 'm-statement__meta'}).find('a').text.strip()
        label = inner_soup.find('div', attrs={'class': 'm-statement__content'}).find('img',
                                                                                        attrs={'class': 'c-image__original'}).get(
            'alt').strip()

        all_data.append((statement, link, date, source, label))

# Convert all_data to a DataFrame
data_df = pd.DataFrame(all_data, columns=['Statement', 'Link', 'Date', 'Source', 'Label'])

# Save the data to a CSV file
csv_filename = "inner_data.csv"
data_df.to_csv(csv_filename, index=False, encoding='utf-8')

print(f"All inner data has been saved to {csv_filename}")




















import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

# Create your views here.

def nifty_fifty(request):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
    }
    URL = 'https://www.nseindia.com/market-data/live-equity-market?symbol=NIFTY%2050'
    print(URL)
    page = requests.get(URL, headers=headers)
    page.raise_for_status()

    # res = requests.get("https://www.nseindia.com/api/live-analysis-variations?index=gainers", headers=headers)
    # res.raise_for_status()
    # all_data = res.json()
    # print(all_data)

    # print(page)

    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify())
    gainers_table_div = soup.find('table', id='equityStockTable')
    print(gainers_table_div)
    gainers_table = gainers_table_div[0].find('table', id='tab1Ganier')
    print(gainers_table)
    losers_table_div = soup.find_all('div', id='tab1_tableLoser')
    losers_table = losers_table_div[0].find('table', id='tab1Loser')
    print(losers_table)
    for gainer_row in gainers_table.tbody.find_all('tr'):
        gainer_columns = gainer_row.find_all('td')
        print("----------- gainer columns ------------")
        print(gainer_columns)

    for loser_row in losers_table.tbody.find_all('tr'):
        loser_columns = loser_row.find_all('td')
        print("----------- loser columns ------------")
        print(loser_columns)
    # gainers_loosers_table = gainers_loosers.find_all()
    # print(gainers_loosers)
    print("----------------")
    # print(gainers_loosers_table)
    return render(request, 'nifty_fifty.html', {'nifty': nifty_fifty})
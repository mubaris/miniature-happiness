import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re
from collections import OrderedDict
from datetime import datetime

data = OrderedDict({
    "Mirae Asset Emerging Bluechip Fund": "https://www.etmoney.com/mutual-funds/mirae-asset-emerging-bluechip-fund-direct-growth/16126",
    "SBI Small Cap Fund": "https://www.etmoney.com/mutual-funds/sbi-small-cap-fund-direct-growth/15354",
    "Axis Small Cap Fund": "https://www.etmoney.com/mutual-funds/axis-small-cap-fund-direct-growth/21859",
    "Canara Robeco Emerging Equities Fund": "https://www.etmoney.com/mutual-funds/canara-robeco-emerging-equities-fund-direct-growth/16144",
    "Motilal Oswal Midcap 30 Fund": "https://www.etmoney.com/mutual-funds/motilal-oswal-midcap-30-fund-direct-growth/23602",
    "Invesco India Mid Cap Fund": "https://www.etmoney.com/mutual-funds/invesco-india-mid-cap-fund-direct-growth/16370",
    "Motilal Oswal Multicap 35 Fund": "https://www.etmoney.com/mutual-funds/motilal-oswal-multicap-35-fund-direct-growth/25645",
    "Axis Midcap Fund": "https://www.etmoney.com/mutual-funds/axis-midcap-direct-plan-growth/15257",
    "Kotak Emerging Equity Fund": "https://www.etmoney.com/mutual-funds/kotak-emerging-equity-fund-direct-growth/16693",
    "Invesco India Contra Fund": "https://www.etmoney.com/mutual-funds/invesco-india-contra-fund-direct-growth/16282",
    "Mirae Asset Large Cap Fund": "https://www.etmoney.com/mutual-funds/mirae-asset-large-cap-fund-direct-growth/16138",
    "Kotak Standard Multicap Fund": "https://www.etmoney.com/mutual-funds/kotak-standard-multicap-fund-direct-growth/16699",
    "Invesco India Growth Opportunities Fund": "https://www.etmoney.com/mutual-funds/invesco-india-growth-opportunities-fund-direct-growth/16333",
    "Axis Focused 25 Fund": "https://www.etmoney.com/mutual-funds/axis-focused-25-direct-plan-growth/15251",
    "Axis Bluechip Fund": "https://www.etmoney.com/mutual-funds/axis-bluechip-fund-direct-plan-growth/15249"
})

json_data = []

df = pd.read_csv('symbols.csv', encoding = "ISO-8859-1")

cache = {}

for fund, url in data.items():
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")
    holdings = soup.find("div", class_="holding-list-modal")
    holdings = holdings.find_all("div", class_="mfScheme-fund-progress")
    equity_pc = float(soup.find('a', attrs={"data-holding-type": "EQUITY"}).find('span').text[:-1])

    holding_data = []

    total_change = 0
    total_holdings = 0

    print("Starting ", fund)

    for comp in holdings:
        value_span = comp.find("span", class_="pull-right")
        value = str(value_span.text).strip()
        value = float(value[:-1])
        value_span.replace_with('')
        name = str(comp.find("p", class_="mfScheme-progress-label").text).strip()

        try:
            if not cache.get(name):
                symbol = list(df[df['Company'].str.match(re.escape(name))]['Symbol'])[0]
                if symbol.startswith("UNK:"):
                    diff = 0
                elif symbol.startswith("IND:"):
                    symbol_new = symbol.replace("IND:", "")
                    data_req = requests.get("https://trendlyne.com/equity/" + symbol_new)
                    data_soup = BeautifulSoup(data_req.text, "lxml")
                    change = data_soup.find("span", class_="LpriceChP")
                    if change:
                        diff = float(change.text)
                    else:
                        diff = 0
                else:
                    data_req = requests.get("https://trendlyne.com/equity/" + symbol)
                    data_soup = BeautifulSoup(data_req.text, "lxml")
                    change = data_soup.find("span", class_="LpriceChP")
                    if change:
                        diff = float(change.text[1:-2])
                    else:
                        diff = 0
                cache[name] = diff
            else:
                diff = cache.get(name)
        except Exception as e:
            symbol = "UNK:X"
            print("Symbol not found for ", name)
            print(e)
            diff = 0
        
        total_change += (diff * value)
        total_holdings += value

        print("Done EQ ", name, " ", diff)

        holding_data.append({"name": name, "pc": value, "symbol": symbol, "diff": diff})
    
    print("Finished ", fund)

    total_change /= total_holdings

    total_change *= (equity_pc / 100)

    total_change += ((100 - equity_pc) * 7 / 365)
    
    json_data.append({"name": fund, "holdings": holding_data, "equity": equity_pc, "change": total_change})

now = datetime.now()

dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

with open('data.json', 'w') as f:
    json.dump({"data": json_data, "date": dt_string}, f)

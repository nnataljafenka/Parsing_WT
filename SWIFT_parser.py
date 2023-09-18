import requests
from lxml import html
import pandas as pd

# константы
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
COUNTRY_URL = 'https://www.theswiftcodes.com/browse-by-country/'
SWIFT_BASE_URL = 'https://www.theswiftcodes.com'


# список всех стран
def get_countries():
    country_response = requests.get(COUNTRY_URL, headers=HEADER)
    countries = []
    if country_response.ok:
        dom = html.fromstring(country_response.text)
        items = dom.xpath("//ol")

        for item in items:
            all_country_item = item.xpath("./li/a/@href")
            countries.extend(all_country_item)
    return countries


def get_swift(countries: list):
    if type(countries) != list:
        raise TypeError("На вход может быть передан только список стран")
    # запуск кракена по всем странам
    for country in countries:
        url = country
        next_page = 'next'
        max_page = ''
        while max_page != next_page:
            swift_url = SWIFT_BASE_URL + url
            response = requests.get(swift_url, headers=HEADER)

            if response.ok:
                dom = html.fromstring(response.text)
                items = dom.xpath("//table[@class='swift-country']")

                for item in items:
                    try:
                        max_page = item.xpath("//a[text()[contains(.,'Last')]]//@href")[0]
                        next_page = item.xpath("//a[text()[contains(.,'Next')]]//@href")[0]
                    except IndexError:
                        max_page = ''
                        next_page = ''
                    bank_name = item.xpath(".//td[2]/text()")
                    city = item.xpath(".//td[3]/text()")
                    swift_code = item.xpath(".//td[5]/a/text()")

                    df = pd.DataFrame({
                        'country': country.upper().strip('/'),
                        'bank_name': bank_name,
                        'city': city,
                        'swift_code': swift_code
                    })

            url = next_page
    return df


countries = get_countries()
df_swift = get_swift(countries[:2])
# print(df_swift)
# df_swift.to_csv('out.csv', mode='a', header=False)

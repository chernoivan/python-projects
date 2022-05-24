import json
from datetime import datetime, timezone
from time import sleep
import requests
from bs4 import BeautifulSoup


# url = "https://www.ahotu.com/advanced-search#activity=run,cycling&month=5,6,4&country=AUS,BEL,CAN,CYP,FRA,GRC,DEU,HKG,IRL,ITA,NZL,SGP,SWE,ESP,ZAF,CHE,ARE,GBR,USA&language=en"
#
# url_json = "https://www.ahotu.com/advanced-search.json?activity[]=run&activity[]=cycling&month[]=5&month[]=6&month[]=4&country[]=AUS&country[]=BEL&country[]=CAN&country[]=CYP&country[]=FRA&country[]=GRC&country[]=DEU&country[]=HKG&country[]=IRL&country[]=ITA&country[]=NZL&country[]=SGP&country[]=SWE&country[]=ESP&country[]=ZAF&country[]=CHE&country[]=ARE&country[]=GBR&country[]=USA&language=en"
#
# headers = {
#     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
# }
#
# src = requests.get(url_json, headers=headers)
#
# print(src.text)
#
# with open("test.json", 'w') as file:
#     json.dump(src.json(), file, indent=4)

def parcer():
    with open("test.json") as file:
        src = json.load(file)

    src = src['races']

    data = []

    for obj in src:
        # print(obj)
        event_name = obj['event_name_en']
        date = (datetime.fromisoformat(obj['start_date'][:-1]).astimezone(timezone.utc)).strftime('%Y-%m-%d')
        country = obj['country']
        location = obj['city']

        link = 'https://www.ahotu.com/event/'+obj['permalink']

        request = requests.get(link)
        with open("index1.html", "w") as file:
            file.write(request.text)

        with open("index1.html") as file:
            file = file.read()

        soup = BeautifulSoup(file, "lxml")
        site_link = soup.find('section', class_="row mt-5 mb-5").find('div', class_='col-12 col-sm-6').find('dd', class_="no-scroll")
        if site_link is None:
            site_link = ''
        else:
            site_link = soup.find('section', class_="row mt-5 mb-5").find('div', class_='col-12 col-sm-6').find('dd', class_="no-scroll").find('a').text


        facebook, inst, twitter, you_tube = '', '', '', ''

        all_a = soup.find('section', class_="row mt-5 mb-5").find_all('a')
        for a in all_a:
            if a.text == "Facebook page":
                print('https://www.ahotu.com/event' + a.get('href'))
                facebook = 'https://www.ahotu.com/event' + a.get('href')
            else:
                facebook = ''

        for a in all_a:
            if a.text == "Instagram":
                print('https://www.ahotu.com/event' + a.get('href'))
                inst = 'https://www.ahotu.com/event' + a.get('href')
            else:
                inst = ''

        for a in all_a:
            if a.text == "Twitter":
                print('https://www.ahotu.com/event' + a.get('href'))
                twitter = 'https://www.ahotu.com/event' + a.get('href')
            else:
                twitter = ''

        for a in all_a:
            if a.text == "You Tube":
                print('https://www.ahotu.com/event' + a.get('href'))
                you_tube = 'https://www.ahotu.com/event' + a.get('href')
            else:
                you_tube = ''

        data.append({
            'event_name': event_name,
            'date': date,
            'country': country,
            'location': location,
            'link': site_link,
            'facebook': facebook,
            'instagram': inst,
            'twitter': twitter,
            'you_tube': you_tube,
        })

    with open("final.json", 'w') as file:
        json.dump(data, file, indent=4)


def main():
    parcer()


if __name__ == '__main__':
    main()

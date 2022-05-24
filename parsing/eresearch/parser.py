import csv
import datetime
import glob
import os
import random
from time import sleep
import bs4
import requests
from xlsxwriter.workbook import Workbook


data_now = datetime.datetime.now()


def days_count():
    date = datetime.datetime(1996, 1, 1)
    now = datetime.datetime.now()
    timedelta = str(now - date)
    timedelta = int(timedelta.split()[0]) + 1

    dates = []

    date = datetime.datetime(1996, 1, 1)

    for i in range(1, timedelta):
        date = date + datetime.timedelta(days=1)
        dates.append(date.strftime("%m/%d/%Y"))

    return dates


def parse_site():
    days = days_count()

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
    }

    iteration = 1

    with open(f"data_{data_now}.csv", "w", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'company',
                'symbol',
                'split_ratio',
                'announcement_date',
                'record_date',
                'ex_date'
            )
        )

    for day in days[1:11]:

        url = f"https://eresearch.fidelity.com/eresearch/conferenceCalls.jhtml?tab=splits&begindate={day}"

        src = requests.get(url=url, headers=headers)
        src = src.text

        data = []

        try:
            soup = bs4.BeautifulSoup(src, "lxml")
            table = soup.find('table', class_='datatable-component events-calender-table-four')
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')

            for row in rows:
                company = row.find('th').find('a').text
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                cols.append(company)
                data.append([ele for ele in cols])

            for d in data:
                with open(f"data_{data_now}.csv", "a", encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        (
                            d[5],
                            d[0],
                            d[1],
                            d[2],
                            d[3],
                            d[4]
                        )
                    )
        except Exception as ex:
            print(f"[ERROR] {ex}!!! For day: 05/02/1996")

        print(f"[INFO] Iteration {iteration}/{len(days)}")
        iteration += 1
        sleep(random.randint(2, 3))


def csv_to_xlsx(data_now):
    for csvfile in glob.glob(os.path.join('.', f'data_{data_now}.csv')):
        workbook = Workbook(csvfile[:-4] + '.xlsx')
        worksheet = workbook.add_worksheet()
        with open(csvfile, 'rt', encoding='utf8') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    worksheet.write(r, c, col)
        workbook.close()


def main():
    parse_site()
    csv_to_xlsx(data_now)


if __name__ == '__main__':
    main()

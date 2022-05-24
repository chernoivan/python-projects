import json
from bs4 import BeautifulSoup


full_info = []

for i in range(0, 1000, 24):

    with open(f"/Users/alex/Documents/repos/parsing/onlyfinder/data/index_{i}.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    accounts = soup.find_all(class_="result")

    for account in accounts:
        username = account.find('div', class_="result-container col-sm-7").find("h3").text
        link = account.find('div', class_="img-avatar-container").find("a").get("href")

        account_info = account.find('div', class_="profile-info").find_all('span', class_="mr-3")
        for photo in account_info:
            if photo.text.find("Photo") == 0:
                number_of_photo = photo.text
                number_of_photo = number_of_photo.split()[-1]

        for video in account_info:
            if video.text.find("Videos") == 0:
                number_of_video = video.text
                number_of_video = number_of_video.split()[-1]

        number_of_posts = str(int(number_of_photo) + int(number_of_video))

        for subscribers in account_info:
            if subscribers.text.find("Likes") == 0:
                number_of_likes = subscribers.text
                number_of_likes = number_of_likes.split()[1:]
                number_of_likes = ''.join(number_of_likes)

        full_info.append(
            {
                'username': username,
                'link': link,
                'num_of_posts': number_of_posts,
                'num_of_likes': number_of_likes,
            }
        )

with open("test.json", 'w', encoding='utf-8') as file:
    json.dump(full_info, file, indent=4, ensure_ascii=False)
import re
import time
import requests
import pandas as pd
import html

def fetch_posts(url):
    all_posts = []
    page = 1
    per_page = 100  # Adjust per_page to a suitable number your server can handle

    while True:
        response = requests.get(url, params={'per_page': per_page, 'page': page})
        posts = response.json()
        if not posts or isinstance(posts, dict):  # A dict response likely indicates an error
            break
        all_posts.extend(posts)
        page += 1

    return all_posts

def main():
    # URL of the WordPress API endpoint
    url = 'https://bizwave.lk/wp-json/wp/v2/posts'

    # Fetch all posts
    posts = fetch_posts(url)

    # Extract required fields
    data = []
    for post in reversed(posts[:-101]):
        #print(post)
        title = html.unescape(post['title']['rendered'])
        content = html.unescape(post['content']['rendered'])
        content = re.sub(r'<\/?p>', '', content)
        trimmed_content = content[1:150]
        link = post['link']
        thumbnail = post['jetpack_featured_media_url']

        message = (f"*{title}*\n{link}\n\n`Facebook:`\nhttps://www.facebook.com/BizWaveLK/\n`LinkedIn:`\nhttps://www.linkedin.com/company/bizwavelk \n`WhatsApp Channel:`\nhttps://whatsapp.com/channel/0029Vaa4Pv33WHTVz4viQ31T\n`Web:`\nhttps://bizwave.lk/")

        url = "https://gate.whapi.cloud/messages/link_preview"

        headers = {
            "accept": "application/json",
            "authorization": "Bearer OX6BKm7qrqNxUB9mJS1OwEzyvYjO98Z5",
            "content-type": "application/json"
        }

        data_1 = {
                "to": "120363279989369450@newsletter",
                "body": message,
                "title": (f"{title}"),
                "canonical": "https://bizwave.lk/",
                "view_once": False,
                "media": (f"{thumbnail}"),
                "description": trimmed_content
        }

        if(title != "Daily Quote" or "Happy New Year"):
            requests.post(url, headers=headers, json=data_1)
            time.sleep(3)
            # data.append({
            #     'Title': title,
            #     'Content': trimmed_content,
            #     'Link': link,
            #     'Thumbnail': thumbnail
            # })

    # Create a DataFrame and write it to an Excel file
    df = pd.DataFrame(data)
    df.to_excel('WordPress_Posts.xlsx', index=False)

if __name__ == "__main__":
    main()

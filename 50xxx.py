import requests
import re


def scrape_m3u8_urls(url):
    # Send a GET request to the website
    response = requests.get(url)
    print(response.text)
    # Check if the request was successful
    if response.status_code == 200:
        # Use regular expressions to find M3U8 URLs
        m3u8_urls = re.findall(r'(?<=\bhref=")(.*?\.mp4\b)', response.text)

        # Print the found URLs
        for m3u8_url in m3u8_urls:
            print(m3u8_url)
    else:
        print("Failed to retrieve website content.")


# Example usage
scrape_m3u8_urls("https://bigbearlake.12milesout.com/video/meeting/2a3a6b53-a01c-4e87-9d22-32c29e692619")
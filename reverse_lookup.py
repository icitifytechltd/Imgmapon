import requests
from bs4 import BeautifulSoup


def reverse_image_search(image_url):
    """
    Performs a Google Images reverse lookup via 'search by image' endpoint.
    (Limited, basic fallback method.)
    """
    try:
        search_url = "https://www.google.com/searchbyimage"
        params = {"image_url": image_url}
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(search_url, params=params, headers=headers, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.title.string if soup.title else "No title"
        guess = soup.find("div", attrs={"class": "r5a77d"})
        return {"title": title, "best_guess": guess.text if guess else "Unknown"}
    except Exception as e:
        return {"error": str(e)}

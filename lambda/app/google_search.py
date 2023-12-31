"""googlesearch is a Python library for searching Google, easily."""
from time import sleep
from bs4 import BeautifulSoup
from requests import get
from .user_agents import get_useragent


def _req(term, results, lang, start, proxies, timeout, cookies=None):
    resp = get(
        url="https://www.google.com/search",
        headers={"User-Agent": get_useragent()},
        params={
            "q": term,
            "num": results + 5,  # Prevents multiple requests
            "hl": lang,
            "start": start,
        },
        proxies=proxies,
        timeout=timeout,
        cookies=cookies,
    )
    resp.raise_for_status()
    return resp


class SearchResult:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"


def search(
    term,
    num_results=10,
    lang="en",
    proxies=None,
    advanced=False,
    sleep_interval=0,
    timeout=5,
    cookies=None,
):
    """Search the Google search engine"""

    escaped_term = term.replace(" ", "+")

    # Fetch
    start = 0
    last = -1
    while start < num_results:
        if last == start:
            break
        last = start
        # Send request
        resp = _req(
            escaped_term,
            num_results - start,
            lang,
            start,
            proxies,
            timeout,
            cookies,
        )

        # Parse
        soup = BeautifulSoup(resp.text, "html.parser")
        result_block = soup.find_all("div", attrs={"class": "g"})
        for result in result_block:
            # Find link, title, description
            link = result.find("a", href=True)
            title = result.find("h3")
            description_box = result.find("div", {"style": "-webkit-line-clamp:2"})
            if description_box:
                description = description_box.text
                if link and title and description:
                    start += 1
                    print('search_result, title:' + title.text + ' desc:' + description)
                    if advanced:
                        yield SearchResult(link["href"], title.text, description)
                    else:
                        yield link["href"]
        sleep(sleep_interval)

import requests
from bs4 import BeautifulSoup


class ForumParser:
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    def parse_page(self, url: str):
        if not isinstance(url, str):
            raise TypeError("url должен быть str")

        if not url:
            raise ValueError("url не может быть пустым")

        response = requests.get(
            url,
            headers=self.HEADERS,
            timeout=10
        )
        response.raise_for_status()

        return self.parse_html(response.text)

    def parse_html(self, html: str):
        if not isinstance(html, str):
            raise TypeError("html должен быть str")

        soup = BeautifulSoup(html, "lxml")
        parsed_data = []

        for comment in soup.select(".comment"):
            comment_id = comment.get("data-comment-id")
            author = comment.select_one(".author")
            message = comment.select_one(".message")

            if comment_id is None or author is None or message is None:
                continue

            try:
                comment_id = int(comment_id)
            except ValueError:
                continue

            parsed_data.append(
                {
                    "id": comment_id,
                    "name": author.get_text(strip=True),
                    "message": message.decode_contents().strip()
                }
            )

        return parsed_data

    def save_to_db(self, parsed_data, repository):
        saved_count = 0

        for item in parsed_data:
            repository.add(
                item["id"],
                item["name"],
                item["message"]
            )
            saved_count += 1

        return saved_count

import requests
from urllib.parse import urlparse
import re

class RequestGuard:

    def __init__(self, url):
        parsed_url = urlparse(url)
        self.domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        self.forbidden = self.parse_robots()

    def parse_robots(self):
        robots_url = f"{self.domain}/robots.txt"
        forbidden_paths = []

        try:
            response = requests.get(robots_url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching {robots_url}: {e}")
            return forbidden_paths

        for line in response.text.splitlines():
            match = re.match(r'^Disallow:\s*(.*)', line.strip())
            if match:
                path = match.group(1).strip()
                if path:
                    forbidden_paths.append(path)

        return forbidden_paths

    def can_follow_link(self, url):
        parsed_url = urlparse(url)
        link_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        if not link_domain.startswith(self.domain):
            return False
        for path in self.forbidden:
            if parsed_url.path.startswith(path):
                return False
        return True

    def make_get_request(url, use_stream = False):
        if self.can_follow_link(url):
            try:
                return requests.get(url, stream=use_stream)
            except requests.RequestException as e:
                print(f"Error making GET request to {url}: {e}")
                return None
        else:
            print(f"Cannot follow link: {url}")
            return None

if __name__ == "__main__":
    pass
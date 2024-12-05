import sys
import csv
import matplotlib.pyplot as plt
import bs4
from urllib.parse import urljoin, urlparse
from collections import defaultdict
from RequestGuard import RequestGuard
import requests



def validate_arguments(args):
    if len(args) < 2:
        print("Error: invalid arguments. Missing command.")
        return False

    command = args[1]

    if command == '-c':
        if len(args) != 5:
            print("Error: invalid arguments. The '-c' command requires 4 parameters: <url> <output filename 1> <output filename 2>.")
            return False
    elif command == '-p':
        if len(args) != 5:
            print("Error: invalid arguments. The '-p' command requires 4 parameters: <url> <output filename 1> <output filename 2>.")
            return False
    elif command == '-i':
        if len(args) != 5:
            print("Error: invalid arguments. The '-i' command requires 4 parameters: <url> <output file prefix> <filter to run>.")
            return False
        valid_filters = {'-s', '-g', '-f', '-m'}
        if args[4] not in valid_filters:
            print("Error: invalid arguments. The '-i' command requires a valid filter: -s (sepia), -g (grayscale), -f (vertical flip), -m (horizontal flip).")
            return False
    else:
        print(f"Error: invalid arguments. Unknown command '{command}'.")
        return False

    return True

def combine_urls(url_full, url_to_join):
    joined = urljoin(url_full, url_to_join)
    return joined



def count_links_with_guard(start_url, output_file_1, output_file_2):
    # Initialize RequestGuard
    guard = RequestGuard(start_url)
    visited_links = set()
    initial_links = set()
    link_counts = {}

    def get_initial_links(url):
        """Fetch and store initial links while respecting the RequestGuard."""
        try:
            if not guard.can_follow_link(url):
                print(f"Blocked by robots.txt: {url}")
                return

            response = guard.make_get_request(url)
            if not response or response.status_code != 200:
                print(f"Failed to fetch initial page: {url}")
                return

            soup = bs4.BeautifulSoup(response.content, "html.parser")
            a_tags = soup.find_all('a')

            for a in a_tags:
                href = a.get('href')
                if not href:
                    continue

                # Resolve relative URLs
                combined_url = urljoin(url, href)
                parsed_url = urlparse(combined_url)

                # Check if the URL is part of the same domain
                if parsed_url.netloc == urlparse(start_url).netloc:
                    if guard.can_follow_link(combined_url):
                        initial_links.add(combined_url)
        except Exception as e:
            print(f"Error fetching initial links from {url}: {e}")
            
    def follow_links_and_count():
        """Follow links from initial_links and increment counts for only those links."""
        for link in initial_links:
            try:
                if not guard.can_follow_link(link):
                    print(f"Blocked by robots.txt: {link}")
                    continue

                if link not in visited_links:
                    response = guard.make_get_request(link)
                    if not response or response.status_code != 200:
                        print(f"Failed to fetch link: {link}")
                        continue

                    soup = bs4.BeautifulSoup(response.content, "html.parser")
                    a_tags = soup.find_all('a')

                    for a in a_tags:
                        href = a.get('href')
                        if not href:
                            continue

                        # Resolve relative URLs
                        combined_url = urljoin(link, href)

                        # Increment count only for initial links
                        if combined_url in initial_links:
                            link_counts[combined_url] = link_counts.get(combined_url, 0) + 1

                    # Mark the link as visited
                    visited_links.add(link)
            except Exception as e:
                print(f"Error following link {link}: {e}")

    get_initial_links(start_url)


    follow_links_and_count()



    print(link_counts)







        # for link in links_to_visit:
        #     if link in link_counts:
        #         link_counts[link] += 1
        #     else:
        #         link_counts[link] = 1




def main():
    if not validate_arguments(sys.argv):
        sys.exit(1)

    command = sys.argv[1]
    if command == '-c':
        start_url = sys.argv[2]
        output_file_1 = sys.argv[3]
        output_file_2 = sys.argv[4]
        count_links_with_guard(start_url, output_file_1, output_file_2)

if __name__ == "__main__":
    main()





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


def count_links(start_url, output_file_1, output_file_2):
    # Initialize RequestGuard
    guard = RequestGuard(start_url)
    
    links_to_visit = [start_url]
    link_counts = {}
    id_counter = 1
    r = requests.get(start_url)
    soup_object = bs4.BeautifulSoup(r.content, features="html.parser")
    a_tags = soup_object.find_all('a')
    for a in a_tags:
        link = a.get('href')
        combined = combine_urls(start_url, link)
        links_to_visit.append(combined)
    print(links_to_visit)
    for link in links_to_visit:
        link_counts[link] = 1
        if link in link_counts:
            link_counts[link] += 1
        else:
            link_counts[link] = 1
    

    # Create a plot
    # plt.figure(figsize=(10, 6))
    # ids = [url_to_id[url] for url in visited_links.keys()]
    # counts = list(visited_links.values())
    # plt.bar(ids, counts, color='skyblue', width=0.5)
    # plt.xlabel("URL ID")
    # plt.ylabel("Visit Count")
    # plt.title("Visited Links Count")
    # plt.tight_layout()
    # plt.savefig(output_file_1)
    # plt.close()

    # Write data to a CSV file
    # with open(output_file_2, 'w', newline='', encoding='utf-8') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['URL ID', 'Count'])
    #     for url, count in visited_links.items():
    #         writer.writerow([url_to_id[url], count])

    print(f"Link count data saved to {output_file_2} and plot saved to {output_file_1}")

def main():
    if not validate_arguments(sys.argv):
        sys.exit(1)

    command = sys.argv[1]
    if command == '-c':
        start_url = sys.argv[2]
        output_file_1 = sys.argv[3]
        output_file_2 = sys.argv[4]
        count_links(start_url, output_file_1, output_file_2)

if __name__ == "__main__":
    main()

# class WebCrawler:
#     def __init__(self, start_url, output_image, output_csv):
#         self.start_url = start_url
#         self.output_image = output_image
#         self.output_csv = output_csv
#         self.request_guard = RequestGuard(start_url)
#         self.visited = defaultdict(int)
#         self.to_visit = []

#     def extract_links(self, html, base_url):
#         soup = bs4.BeautifulSoup(html, "html.parser")
#         links = []
#         for a_tag in soup.find_all("a", href=True):
#             href = a_tag["href"]
#             if href.startswith("http"):  # Absolute link
#                 links.append(href)
#             elif href.startswith("/"):  # Relative link
#                 links.append(base_url + href)
#         return links

#     def count_links(self):
#         self.to_visit.append(self.start_url)

#         while self.to_visit:
#             current_url = self.to_visit.pop()
#             if current_url in self.visited:
#                 self.visited[current_url] += 1
#                 continue

#             if not self.request_guard.can_follow_link(current_url):
#                 print(f"Skipping disallowed link: {current_url}")
#                 continue

#             try:
#                 response = requests.get(current_url)
#                 response.raise_for_status()
#             except requests.RequestException as e:
#                 print(f"Failed to fetch {current_url}: {e}")
#                 continue

#             self.visited[current_url] += 1
#             new_links = self.extract_links(response.text, self.request_guard.domain)
#             self.to_visit.extend(new_links)

#     def save_histogram(self):
#         counts = list(self.visited.values())
#         plt.hist(counts, bins=range(1, max(counts) + 2), align='left', edgecolor='black')
#         plt.xlabel("Number of Visits")
#         plt.ylabel("Frequency")
#         plt.title("Link Visit Frequency Histogram")
#         plt.savefig(self.output_image)
#         plt.close()

#     def save_csv(self):
#         with open(self.output_csv, "w", newline="") as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerow(["URL", "Count"])
#             for url, count in self.visited.items():
#                 writer.writerow([url, count])

#     def run(self):
#         self.count_links()
#         self.save_histogram()
#         self.save_csv()

# # Main function to handle arguments
# def main():
#     if len(sys.argv) != 5 or sys.argv[1] != "-c":
#         print("Invalid arguments. Usage: -c <url> <output_image> <output_csv>")
#         return

#     url = sys.argv[2]
#     output_image = sys.argv[3]
#     output_csv = sys.argv[4]

#     crawler = WebCrawler(url, output_image, output_csv)
#     crawler.run()
#     print(f"Link counting completed. Results saved to {output_image} and {output_csv}.")

# if __name__ == "__main__":
#     main()




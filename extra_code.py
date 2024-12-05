# def count_links(start_url, output_file_1, output_file_2):
#     # Define the allowed domain
#     allowed_domain = "cs111.byu.edu"
    
#     # Initialize a set to track visited links and a list for links to visit
#     visited = set()
#     links_to_visit = [start_url]
#     link_counts = {}
    
#     while links_to_visit:
#         current_url = links_to_visit.pop(0)
        
#         # Skip if already visited
#         if current_url in visited:
#             continue
        
#         visited.add(current_url)
        
#         try:
#             response = requests.get(current_url)
#             response.raise_for_status()  # Raise HTTPError for bad responses
#         except requests.RequestException as e:
#             print(f"Error fetching {current_url}: {e}")
#             continue
        
#         # Parse the page and find all <a> tags
#         soup = bs4.BeautifulSoup(response.content, "html.parser")
#         a_tags = soup.find_all('a')
        
#         for a in a_tags:
#             href = a.get('href')
#             if not href:
#                 continue
            
#             # Combine URLs
#             combined_url = urljoin(current_url, href)
#             parsed_url = urlparse(combined_url)
            
#             # Check if the URL's domain matches the allowed domain
#             if parsed_url.netloc != allowed_domain:
#                 continue
            
#             # Count links
#             if combined_url in link_counts:
#                 link_counts[combined_url] += 1
#             else:
#                 link_counts[combined_url] = 1
            
#             # Add internal links to the queue
#             if combined_url not in visited:
#                 links_to_visit.append(combined_url)
#     print(link_counts)

# def get_links(url):
#     r = requests.get(url)
#     soup_object = bs4.BeautifulSoup(r.content, features="html.parser")
#     parsed = urlparse(url)
#     if parsed.netloc == 'https://cs111.byu.edu/':
#         ...






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

# print(f"Link count data saved to {output_file_2} and plot saved to {output_file_1}")
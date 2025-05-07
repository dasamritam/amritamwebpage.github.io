import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os
from typing import List, Dict
import time

class ScholarSync:
    def __init__(self, scholar_id: str):
        self.scholar_id = scholar_id
        self.base_url = f"https://scholar.google.com/citations?user={scholar_id}&hl=en"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_publications(self) -> List[Dict]:
        publications = []
        page = 1
        print(f"Fetching publications from Google Scholar...")
        while True:
            url = f"{self.base_url}&view_op=list_works&sortby=pubdate&cstart={(page-1)*20}"
            print(f"Fetching page {page}...")
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                print(f"Error: Got status code {response.status_code}")
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            pub_items = soup.find_all('tr', class_='gsc_a_tr')

            if not pub_items:
                print("No more publications found.")
                break

            for item in pub_items:
                title_elem = item.find('a', class_='gsc_a_t')
                if not title_elem:
                    continue

                title = title_elem.text.strip()
                authors = item.find('div', class_='gs_gray').text.strip()
                venue = item.find('div', class_='gs_gray').find_next('div', class_='gs_gray').text.strip()
                year = item.find('span', class_='gsc_a_h').text.strip()

                if not year.isdigit():
                    continue

                publications.append({
                    'title': title,
                    'authors': authors,
                    'venue': venue,
                    'year': int(year)
                })
                print(f"Found publication: {title}")

            # For testing, only fetch one page
            break

            page += 1
            time.sleep(2)  # Be nice to Google Scholar

        print(f"Found {len(publications)} publications total.")
        return publications

    def generate_markdown(self, publications: List[Dict]) -> str:
        # Group publications by year
        publications_by_year = {}
        for pub in publications:
            year = pub['year']
            if year not in publications_by_year:
                publications_by_year[year] = []
            publications_by_year[year].append(pub)

        # Sort years in descending order
        years = sorted(publications_by_year.keys(), reverse=True)

        markdown = """---
layout: single
author_profile: true
title: "Publications"
toc: false
classes: wide
---

<html>
<head>
  <meta charset="UTF-8">
  <title>Amritam Das - Publication List</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; }
    h2 { margin-top: 0; }
    .author-highlight { font-weight: bold; }
    .title-italic { font-style: italic; }
    .venue, .year { color: #597; }
    .pub-link { color: #1A0DAB; text-decoration: none; }
    .theme-tags { margin-left: 10px; }
.tag {
  display: inline-block;
  background: #e8eaea;
  color: #356;
  border-radius: 0.3em;
  font-size: 0.85em;
  padding: 1px 6px;
  margin-right: 4px;
  font-family: Arial, sans-serif;
}
.tag.nonlinear { background: #FFDD99; color: #875300; }
.tag.pde { background: #CCE5FF; color: #003366; }
.tag.ml { background: #D4EDDA; color: #155724; }
.tag.fault { background: #F8D7DA; color: #721c24; }
  </style>
</head>
<body>
"""

        # Add publications by year
        for year in years:
            markdown += f"\n  <h2>{year}</h2>\n  <ol>\n"
            for pub in publications_by_year[year]:
                # Highlight your name in authors
                authors = pub['authors'].replace('Amritam Das', '<span class="author-highlight">Amritam Das</span>')
                
                # Extract DOI if available in venue
                doi = ""
                if "doi.org" in pub['venue']:
                    doi_match = re.search(r'doi\.org/([^\s]+)', pub['venue'])
                    if doi_match:
                        doi = doi_match.group(1)
                        pub['venue'] = pub['venue'].replace(f"doi.org/{doi}", "").strip()
                
                # Add DOI link if available
                doi_link = f' [<a href="https://doi.org/{doi}">DOI</a>]' if doi else ""
                
                # Add theme tags based on keywords in title and venue
                theme_tags = []
                if any(word in pub['title'].lower() for word in ['nonlinear', 'oscillation', 'trajectory']):
                    theme_tags.append('<span class="tag nonlinear">Nonlinear Control</span>')
                if any(word in pub['title'].lower() for word in ['pde', 'partial', 'distributed']):
                    theme_tags.append('<span class="tag pde">Control of PDEs</span>')
                if any(word in pub['title'].lower() for word in ['learning', 'neural', 'ml']):
                    theme_tags.append('<span class="tag ml">Machine Learning</span>')
                if any(word in pub['title'].lower() for word in ['fault', 'diagnosis']):
                    theme_tags.append('<span class="tag fault">Fault Diagnosis</span>')
                
                theme_tags_html = f' <span class="theme-tags">{" ".join(theme_tags)}</span>' if theme_tags else ""
                
                markdown += f"""    <li>{authors}. <span class="title-italic">{pub['title']}</span>. <span class="venue">{pub['venue']}</span>. {year}.{doi_link}{theme_tags_html}</li>\n"""
            
            markdown += "  </ol>\n"

        markdown += """</body>
</html>"""

        return markdown

    def update_publications_file(self):
        print("Starting publication update...")
        publications = self.get_publications()
        print("Generating markdown content...")
        markdown_content = self.generate_markdown(publications)
        
        output_file = 'publications_new.md'
        print(f"Writing to {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"Done! New publications file created at {output_file}")

if __name__ == "__main__":
    # Replace with your Google Scholar ID
    scholar_id = "dZ1NkwoAAAAJ"
    sync = ScholarSync(scholar_id)
    sync.update_publications_file() 
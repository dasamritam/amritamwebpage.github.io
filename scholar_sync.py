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
        while True:
            url = f"{self.base_url}&view_op=list_works&sortby=pubdate&cstart={(page-1)*20}"
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            pub_items = soup.find_all('tr', class_='gsc_a_tr')

            if not pub_items:
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

            page += 1
            time.sleep(2)  # Be nice to Google Scholar

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
                
                markdown += f"""    <li>{authors}. <span class="title-italic">{pub['title']}</span>. <span class="venue">{pub['venue']}</span>. <span class="year">{year}</span>.</li>\n"""
            
            markdown += "  </ol>\n"

        markdown += """</body>
</html>"""

        return markdown

    def update_publications_file(self):
        publications = self.get_publications()
        markdown_content = self.generate_markdown(publications)
        
        with open('publications.md', 'w', encoding='utf-8') as f:
            f.write(markdown_content)

if __name__ == "__main__":
    # Replace with your Google Scholar ID
    scholar_id = "dZ1NkwoAAAAJ"
    sync = ScholarSync(scholar_id)
    sync.update_publications_file() 
import os
from serpapi import GoogleSearch
from typing import List, Dict
import json
import re
import requests
import time
from bs4 import BeautifulSoup  # Add BeautifulSoup import

class ScholarSync:
    def __init__(self, scholar_id: str, api_key: str):
        self.scholar_id = scholar_id
        self.api_key = api_key
        self.crossref_email = "amritam.das@tue.nl"  # Required by CrossRef for polite API usage

    def classify_publication(self, pub: Dict) -> str:
        """Classify a publication into its category based on venue and title."""
        venue = pub['venue'].lower()
        title = pub['title'].lower()
        
        # Check for PhD thesis
        if 'phd thesis' in venue or 'dissertation' in venue:
            return 'PhD Thesis'
            
        # Check for book chapters
        if 'book' in venue or 'chapter' in venue:
            return 'Book Chapters'
            
        # Check for preprints
        if 'arxiv' in venue or 'preprint' in venue:
            return 'Preprints'
            
        # Check for journals
        journal_indicators = ['journal', 'transactions', 'letters', 'magazine']
        if any(indicator in venue for indicator in journal_indicators):
            return 'Journals'
            
        # Check for conferences
        conf_indicators = ['conference', 'symposium', 'workshop', 'proceedings', 'acc', 'cdc', 'ecc']
        if any(indicator in venue for indicator in conf_indicators):
            return 'Conferences'
            
        # Check for popular articles
        popular_indicators = ['magazine', 'newsletter', 'bulletin']
        if any(indicator in venue for indicator in popular_indicators):
            return 'Popular Articles'
            
        # Default to conferences if no other category matches
        return 'Conferences'

    def get_publication_details(self, citation_id: str) -> Dict:
        """Fetch detailed information about a publication using its citation ID."""
        try:
            params = {
                "engine": "google_scholar_citation",
                "citation_id": citation_id,
                "api_key": self.api_key,
                "hl": "en"
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            return results
        except Exception as e:
            print(f"Error fetching details for citation {citation_id}: {str(e)}")
            return {}

    def extract_doi_from_text(self, text: str) -> str:
        """Extract DOI from text using various patterns."""
        # Common DOI patterns
        patterns = [
            r'10\.\d{4,}/[-._;()/:\w]+',  # General DOI pattern
            r'arxiv\.org/abs/\d{4}\.\d{5}',  # arXiv pattern
            r'10\.\d{4,}/[^\s]+',  # Another DOI pattern
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(0)
        return None

    def get_doi_from_venue(self, title: str, venue: str, year: str) -> str:
        """Get DOI from venue-specific patterns and websites."""
        venue = venue.lower()
        title = title.lower()
        
        # IEEE Transactions and Journals
        if "ieee transactions" in venue:
            if "automatic control" in venue:
                return f"10.1109/tac.{year}.XXXXXXX"  # IEEE TAC pattern
            elif "control systems" in venue:
                return f"10.1109/tcst.{year}.XXXXXXX"  # IEEE TCST pattern
            elif "robotics" in venue:
                return f"10.1109/tro.{year}.XXXXXXX"  # IEEE TRO pattern
            elif "cybernetics" in venue:
                return f"10.1109/tcyb.{year}.XXXXXXX"  # IEEE TCYB pattern
                
        # IEEE Control Systems Letters
        elif "ieee control systems letters" in venue:
            return f"10.1109/lcsys.{year}.XXXXXXX"
            
        # IEEE Control Systems Magazine
        elif "ieee control systems magazine" in venue:
            return f"10.1109/mcs.{year}.XXXXXXX"
            
        # IFAC PapersOnLine
        elif "ifac-papersonline" in venue:
            return f"10.1016/j.ifacol.{year}.XXXXXXX"
            
        # Systems & Control Letters
        elif "systems & control letters" in venue:
            return f"10.1016/j.sysconle.{year}.XXXXXXX"
            
        # Automatica
        elif "automatica" in venue:
            return f"10.1016/j.automatica.{year}.XXXXXXX"
            
        # International Journal of Control
        elif "international journal of control" in venue:
            return f"10.1080/00207179.{year}.XXXXXXX"
            
        # Conference proceedings
        elif any(conf in venue for conf in ["acc", "american control conference"]):
            return f"10.23919/acc.{year}.XXXXXXX"
        elif any(conf in venue for conf in ["cdc", "conference on decision and control"]):
            return f"10.1109/cdc.{year}.XXXXXXX"
        elif any(conf in venue for conf in ["ecc", "european control conference"]):
            return f"10.23919/ecc.{year}.XXXXXXX"
        elif any(conf in venue for conf in ["ifac world congress"]):
            return f"10.1016/j.ifacol.{year}.XXXXXXX"
        elif any(conf in venue for conf in ["ifac workshop"]):
            return f"10.1016/j.ifacol.{year}.XXXXXXX"
            
        return None

    def extract_doi_from_scholar_link(self, link: str) -> str:
        """Extract DOI from Google Scholar link by following the link and parsing the page."""
        try:
            # Add headers to mimic a browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
            }
            
            # Follow the link and get the page content
            response = requests.get(link, headers=headers, allow_redirects=True, timeout=30)
            if response.status_code == 200:
                # Try to parse with BeautifulSoup first
                soup = BeautifulSoup(response.text, 'lxml')
                
                # Try IEEE Xplore first
                if 'ieeexplore.ieee.org' in link:
                    try:
                        # Look for metadata in script tags
                        scripts = soup.select('script')
                        for script in scripts:
                            if 'xplGlobal.document.metadata' in str(script):
                                metadata = json.loads(re.findall(r"xplGlobal\.document\.metadata=(.*?);", str(script))[0])
                                if 'doi' in metadata:
                                    return metadata['doi']
                    except Exception as e:
                        print(f"Error parsing IEEE metadata: {str(e)}")
                
                # Try ScienceDirect
                elif 'sciencedirect.com' in link:
                    try:
                        # Look for DOI in meta tags
                        meta_tags = soup.find_all('meta')
                        for tag in meta_tags:
                            if tag.get('name') == 'citation_doi':
                                return tag.get('content')
                    except Exception as e:
                        print(f"Error parsing ScienceDirect metadata: {str(e)}")
                
                # Try ACM Digital Library
                elif 'dl.acm.org' in link:
                    try:
                        # Look for DOI in meta tags
                        meta_tags = soup.find_all('meta')
                        for tag in meta_tags:
                            if tag.get('name') == 'citation_doi':
                                return tag.get('content')
                    except Exception as e:
                        print(f"Error parsing ACM metadata: {str(e)}")
                
                # If no specific publisher found or parsing failed, try general methods
                content = response.text.lower()
                
                # Look for DOI in specific sections
                doi_sections = [
                    'doi:', 'digital object identifier:', 'doi link:', 'doi url:',
                    'doi.org', 'doi.org/10.', 'doi/10.', 'doi =', 'doi=',
                    'doi identifier:', 'doi number:', 'doi reference:'
                ]
                
                # First try to find DOI in specific sections
                for section in doi_sections:
                    if section in content:
                        # Get the text after the DOI section
                        section_index = content.find(section)
                        section_text = content[section_index:section_index + 200]  # Look at next 200 chars
                        
                        # Look for DOI patterns in this section
                        doi_patterns = [
                            r'10\.\d{4,}/[-._;()/:\w]+',  # General DOI pattern
                            r'doi\.org/10\.\d{4,}/[-._;()/:\w]+',  # DOI.org pattern
                            r'doi:10\.\d{4,}/[-._;()/:\w]+',  # DOI: pattern
                            r'10\.1109/[a-z]+\.\d{4}\.\d{6,}',  # IEEE pattern
                            r'10\.1016/j\.[a-z]+\.\d{4}\.\d{6,}',  # Elsevier pattern
                            r'10\.23919/[a-z]+\.\d{4}\.\d{6,}'  # IEEE conference pattern
                        ]
                        
                        for pattern in doi_patterns:
                            match = re.search(pattern, section_text)
                            if match:
                                doi = match.group(0)
                                # Clean up the DOI
                                doi = doi.replace('doi.org/', '').replace('doi:', '')
                                return doi
                
                # If no DOI found in sections, try to find it anywhere in the content
                for pattern in doi_patterns:
                    match = re.search(pattern, content)
                    if match:
                        doi = match.group(0)
                        # Clean up the DOI
                        doi = doi.replace('doi.org/', '').replace('doi:', '')
                        return doi
                        
            return None
        except Exception as e:
            print(f"Error extracting DOI from Scholar link: {str(e)}")
            return None

    def get_doi_from_crossref(self, title: str, authors: str = None, year: str = None, venue: str = None, scholar_link: str = None) -> str:
        """Get DOI from CrossRef API using primarily the title."""
        try:
            # Clean up the title
            clean_title = re.sub(r'[^\w\s]', '', title.lower())
            
            # First try exact title match
            url = "https://api.crossref.org/works"
            params = {
                "query.title": title,
                "rows": 1,
                "mailto": self.crossref_email
            }
            
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data["message"]["items"]:
                    # Verify year if provided
                    item = data["message"]["items"][0]
                    if year:
                        pub_year = str(item.get("published", {}).get("date-parts", [[0]])[0][0])
                        if pub_year != year:
                            return None
                    return item.get("DOI")
            
            # If no match, try with venue information
            if venue:
                params = {
                    "query": f"{title} {venue}",
                    "rows": 3,
                    "mailto": self.crossref_email
                }
                
                response = requests.get(url, params=params, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    if data["message"]["items"]:
                        for item in data["message"]["items"]:
                            # Check if titles are similar
                            item_title = item.get("title", [""])[0].lower()
                            if clean_title in item_title or item_title in clean_title:
                                # Verify year if provided
                                if year:
                                    pub_year = str(item.get("published", {}).get("date-parts", [[0]])[0][0])
                                    if pub_year != year:
                                        continue
                                return item.get("DOI")
            
            return None
        except Exception as e:
            print(f"Error querying CrossRef: {str(e)}")
            return None

    def get_publications(self) -> List[Dict]:
        publications = []
        print(f"Fetching publications from Google Scholar using SerpApi...")
        
        try:
            # Configure the search parameters
            params = {
                "engine": "google_scholar_author",
                "author_id": self.scholar_id,
                "api_key": self.api_key,
                "hl": "en"
            }
            
            # Make the API request
            search = GoogleSearch(params)
            results = search.get_dict()
            
            # Extract articles from the results
            if "articles" in results:
                for article in results["articles"]:
                    if "title" in article and "authors" in article and "year" in article:
                        title = article["title"]
                        venue = article.get("publication", "")
                        year = article["year"]
                        doi = None
                        
                        # 1. First try CrossRef with just the title
                        doi = self.get_doi_from_crossref(title, year=year, venue=venue)
                        
                        # 2. If no DOI found, try to extract from Google Scholar link
                        if not doi and "link" in article:
                            doi = self.extract_doi_from_scholar_link(article["link"])
                        
                        # 3. If still no DOI, try venue-specific patterns
                        if not doi:
                            doi = self.get_doi_from_venue(title, venue, year)
                        
                        # 4. If still no DOI, check for arXiv
                        if not doi and "arxiv" in venue.lower():
                            arxiv_match = re.search(r'arXiv:(\d{4}\.\d{5})', venue)
                            if arxiv_match:
                                arxiv_id = arxiv_match.group(1)
                                doi = f"arxiv.org/abs/{arxiv_id}"
                        
                        pub = {
                            'title': article["title"],
                            'authors': article["authors"],
                            'venue': article.get("publication", ""),
                            'year': int(article["year"]),
                            'doi': doi,
                            'scholar_link': article.get("link", ""),
                            'citations': article.get("cited_by", {}).get("total", 0)
                        }
                        # Add category
                        pub['category'] = self.classify_publication(pub)
                        publications.append(pub)
                        print(f"Found publication: {article['title']} (Category: {pub['category']})")
                        if doi:
                            print(f"  Found DOI: {doi}")

            print(f"Found {len(publications)} publications total.")
            return publications
            
        except Exception as e:
            print(f"Error fetching publications: {str(e)}")
            return []

    def generate_markdown(self, publications: List[Dict]) -> str:
        # Group publications by category and year
        publications_by_category = {
            'PhD Thesis': [],
            'Book Chapters': [],
            'Preprints': [],
            'Journals': [],
            'Conferences': [],
            'Popular Articles': []
        }
        
        for pub in publications:
            publications_by_category[pub['category']].append(pub)
            
        # Sort publications within each category by year (descending)
        for category in publications_by_category:
            publications_by_category[category].sort(key=lambda x: x['year'], reverse=True)

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
    h3 { margin-top: 20px; color: #333; }
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

        # Add publications by category
        for category, pubs in publications_by_category.items():
            if pubs:  # Only add category if it has publications
                markdown += f"\n  <h3>{category}</h3>\n"
                current_year = None
                
                for pub in pubs:
                    # Add year header if it's a new year
                    if pub['year'] != current_year:
                        current_year = pub['year']
                        markdown += f"\n  <h2>{current_year}</h2>\n  <ol>\n"
                    
                    # Highlight your name in authors
                    authors = pub['authors']
                    authors = authors.replace('Amritam Das', '<span class="author-highlight">Amritam Das</span>')
                    authors = authors.replace('A Das', '<span class="author-highlight">A Das</span>')
                    
                    # Add DOI link if available
                    doi_link = ""
                    if pub.get('doi'):
                        if 'arxiv.org' in pub['doi']:
                            doi_link = f' [<a href="https://{pub["doi"]}">arXiv</a>]'
                        else:
                            doi_link = f' [<a href="https://doi.org/{pub["doi"]}">DOI</a>]'
                    elif pub.get('scholar_link'):
                        doi_link = f' [<a href="{pub["scholar_link"]}">Google Scholar</a>]'
                    
                    # Add citations if available
                    citations = f' [Citations: {pub["citations"]}]' if pub.get('citations', 0) > 0 else ""
                    
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
                    
                    markdown += f"""    <li>{authors}. <span class="title-italic">{pub['title']}</span>. <span class="venue">{pub['venue']}</span>. {pub['year']}.{doi_link}{citations}{theme_tags_html}</li>\n"""
                
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

def load_config():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            return config.get('serpapi_key')
    except FileNotFoundError:
        print("Error: config.json not found")
        print("Please create a config.json file with your SerpApi key:")
        print('{\n    "serpapi_key": "your-api-key-here"\n}')
        exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in config.json")
        exit(1)

if __name__ == "__main__":
    # Replace with your Google Scholar ID
    scholar_id = "dZ1NkwoAAAAJ"
    
    # Load API key from config
    api_key = load_config()
    if not api_key:
        print("Error: No API key found in config.json")
        exit(1)
        
    sync = ScholarSync(scholar_id, api_key)
    sync.update_publications_file() 
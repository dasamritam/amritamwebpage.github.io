import os
from scholarly import scholarly
from typing import List, Dict
import json
import re
import requests
import time
from bs4 import BeautifulSoup
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ScholarSync:
    def __init__(self, scholar_id: str):
        self.scholar_id = scholar_id
        self.crossref_email = "amritam.das@tue.nl"  # Required by CrossRef for polite API usage
        self._setup_browser()

    def _setup_browser(self):
        """Set up Chrome browser for Google Scholar access."""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920x1080')
            
            # Add more realistic browser configuration
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Add more realistic user agent
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
            
            # Add additional headers
            chrome_options.add_argument('--accept-language=en-US,en;q=0.9')
            chrome_options.add_argument('--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Execute CDP commands to make automation less detectable
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            })
            
            # Add additional properties to make automation less detectable
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("Browser setup completed successfully")
            return True
        except Exception as e:
            print(f"Error setting up browser: {str(e)}")
            return False

    def _get_publications_from_scholar(self):
        """Fetch publications directly from Google Scholar using Selenium."""
        max_retries = 3
        retry_delay = 5  # seconds
        publications = []
        page = 0
        
        while True:  # Continue until no more pages
            for attempt in range(max_retries):
                try:
                    url = f"https://scholar.google.com/citations?user={self.scholar_id}&hl=en&cstart={page*100}&pagesize=100"
                    print(f"Attempting to fetch publications page {page + 1} (attempt {attempt + 1}/{max_retries})...")
                    
                    self.driver.get(url)
                    time.sleep(random.uniform(2, 4))  # Random delay before proceeding
                    
                    # Wait for publications to load
                    try:
                        WebDriverWait(self.driver, 15).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "gsc_a_tr"))
                        )
                    except Exception as e:
                        print(f"Error waiting for publications to load: {str(e)}")
                        if "This page appears to be sending automated queries" in self.driver.page_source:
                            print("Google Scholar detected automated access. Retrying...")
                            time.sleep(retry_delay * (attempt + 1))
                            continue
                        raise e
                    
                    pub_elements = self.driver.find_elements(By.CLASS_NAME, "gsc_a_tr")
                    if not pub_elements:  # No more publications
                        return publications
                        
                    print(f"Found {len(pub_elements)} publications on page {page + 1}")
                    
                    for element in pub_elements:
                        try:
                            title = element.find_element(By.CLASS_NAME, "gsc_a_at").text
                            authors = element.find_element(By.CLASS_NAME, "gs_gray").text
                            venue = element.find_elements(By.CLASS_NAME, "gs_gray")[1].text
                            year = element.find_element(By.CLASS_NAME, "gsc_a_y").text
                            link = element.find_element(By.CLASS_NAME, "gsc_a_at").get_attribute("href")
                            
                            if not title or not authors:  # Skip entries with missing essential info
                                continue
                                
                            pub = {
                                'title': title,
                                'authors': authors,
                                'venue': venue,
                                'year': int(year) if year.isdigit() else 0,
                                'scholar_link': link
                            }
                            publications.append(pub)
                            print(f"Processed: {title[:50]}...")
                            
                            # Add a small random delay between publications
                            time.sleep(random.uniform(0.5, 1))
                            
                        except Exception as e:
                            print(f"Error processing publication element: {str(e)}")
                            continue
                    
                    if pub_elements:  # If we successfully got publications, break the retry loop
                        break
                        
                except Exception as e:
                    print(f"Error during attempt {attempt + 1}: {str(e)}")
                    if attempt < max_retries - 1:
                        print(f"Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay * (attempt + 1))
                    else:
                        print("Max retries reached. Unable to fetch publications.")
                        raise e
            
            # Check if there are more pages
            try:
                next_button = self.driver.find_element(By.ID, "gsc_bpf_next")
                if "disabled" in next_button.get_attribute("class"):
                    break
                page += 1
                time.sleep(random.uniform(2, 4))  # Random delay between pages
            except:
                break
                
        return publications

    def get_publications(self) -> List[Dict]:
        print(f"Fetching publications from Google Scholar...")
        
        try:
            publications = self._get_publications_from_scholar()
            processed_publications = []
            
            for pub in publications:
                try:
                    title = pub['title']
                    venue = pub['venue']
                    year = str(pub['year'])
                    doi = None
                    
                    # Try to get DOI from CrossRef
                    doi = self.get_doi_from_crossref(title, year=year, venue=venue)
                    
                    # If no DOI found, try to extract from Google Scholar link
                    if not doi and pub.get('scholar_link'):
                        doi = self.extract_doi_from_scholar_link(pub['scholar_link'])
                    
                    # If still no DOI, try venue-specific patterns
                    if not doi:
                        doi = self.get_doi_from_venue(title, venue, year)
                    
                    # If still no DOI, check for arXiv
                    if not doi and 'arxiv' in venue.lower():
                        arxiv_match = re.search(r'arXiv:(\d{4}\.\d{5})', venue)
                        if arxiv_match:
                            arxiv_id = arxiv_match.group(1)
                            doi = f"arxiv.org/abs/{arxiv_id}"
                    
                    pub_data = {
                        'title': title,
                        'authors': pub['authors'],
                        'venue': venue,
                        'year': int(year) if year.isdigit() else 0,
                        'doi': doi,
                        'scholar_link': pub.get('scholar_link', '')
                    }
                    
                    # Add category
                    pub_data['category'] = self.classify_publication(pub_data)
                    processed_publications.append(pub_data)
                    print(f"Found publication: {title} (Category: {pub_data['category']})")
                    if doi:
                        print(f"  Found DOI: {doi}")
                    
                except Exception as e:
                    print(f"Error processing publication: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error fetching publications: {str(e)}")
            return []
        finally:
            try:
                self.driver.quit()
            except:
                pass

        print(f"Found {len(processed_publications)} publications total.")
        return processed_publications

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
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
            }
            
            # Follow the link and get the page content
            response = requests.get(link, headers=headers, allow_redirects=True, timeout=30)
            if response.status_code == 200:
                # Try to parse with BeautifulSoup
                soup = BeautifulSoup(response.text, 'lxml')
                
                # Try publisher-specific extraction first
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
                
                elif 'sciencedirect.com' in link:
                    try:
                        # Look for DOI in meta tags
                        meta_tags = soup.find_all('meta')
                        for tag in meta_tags:
                            if tag.get('name') == 'citation_doi':
                                return tag.get('content')
                    except Exception as e:
                        print(f"Error parsing ScienceDirect metadata: {str(e)}")
                
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
                                # Validate DOI format
                                if re.match(r'^10\.\d{4,}/[-._;()/:\w]+$', doi):
                                    return doi
                
                # If no DOI found in sections, try to find it anywhere in the content
                for pattern in doi_patterns:
                    match = re.search(pattern, content)
                    if match:
                        doi = match.group(0)
                        # Clean up the DOI
                        doi = doi.replace('doi.org/', '').replace('doi:', '')
                        # Validate DOI format
                        if re.match(r'^10\.\d{4,}/[-._;()/:\w]+$', doi):
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

    def generate_markdown_content(self, publications):
        """Generate markdown content with proper HTML formatting."""
        content = """---
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
    .venue { color: #597; }
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
    ol { margin: 0; padding: 0; }
    li { margin: 0; padding: 0; }
  </style>
</head>
<body>"""

        # Group publications by category and year
        categories = {
            'PhD Thesis': [],
            'Preprints': [],
            'Journals': [],
            'Conferences': []
        }

        for pub in publications:
            categories[pub['category']].append(pub)

        # Sort publications within each category by year (descending)
        for category in categories:
            categories[category].sort(key=lambda x: x['year'], reverse=True)

        # Generate content for each category
        for category, pubs in categories.items():
            if not pubs:
                continue

            content += f"\n<h3>{category}</h3>"
            current_year = None

            for pub in pubs:
                if pub['year'] != current_year:
                    if current_year is not None:
                        content += "</ol>"
                    current_year = pub['year']
                    content += f"\n<h2>{current_year}</h2>\n<ol>"

                # Format authors
                authors = pub['authors'].split(', ')
                authors = [f'<span class="author-highlight">A Das</span>' if 'A Das' in author else author for author in authors]
                authors_str = ', '.join(authors)

                # Format title
                title = f'<span class="title-italic">{pub["title"]}</span>'

                # Format venue
                venue = f'<span class="venue">{pub["venue"]}</span>'

                # Format links
                links = []
                if pub.get('doi'):
                    # Check if it's an arXiv ID
                    if pub['doi'].startswith('arxiv.org/abs/'):
                        arxiv_id = pub['doi'].replace('arxiv.org/abs/', '')
                        links.append(f'[<a href="https://arxiv.org/abs/{arxiv_id}">arXiv</a>]')
                    # Check if it's a placeholder DOI
                    elif 'XXXXXXX' in pub['doi']:
                        # Try to get the actual DOI from CrossRef
                        actual_doi = self.get_doi_from_crossref(pub['title'], year=str(pub['year']), venue=pub['venue'])
                        if actual_doi:
                            links.append(f'[<a href="https://doi.org/{actual_doi}">DOI</a>]')
                        else:
                            links.append(f'[<a href="{pub.get("scholar_link", "#")}">Google Scholar</a>]')
                    else:
                        # Clean up the DOI
                        doi = pub['doi'].replace('doi.org/', '').replace('doi:', '')
                        links.append(f'[<a href="https://doi.org/{doi}">DOI</a>]')
                elif pub.get('scholar_link'):
                    links.append(f'[<a href="{pub["scholar_link"]}">Google Scholar</a>]')
                links_str = ' '.join(links)

                # Format tags
                tags = []
                if 'Control of PDEs' in pub.get('tags', []):
                    tags.append('<span class="tag pde">Control of PDEs</span>')
                if 'Nonlinear Control' in pub.get('tags', []):
                    tags.append('<span class="tag nonlinear">Nonlinear Control</span>')
                if 'Machine Learning' in pub.get('tags', []):
                    tags.append('<span class="tag ml">Machine Learning</span>')
                if 'Fault Diagnosis' in pub.get('tags', []):
                    tags.append('<span class="tag fault">Fault Diagnosis</span>')
                tags_str = f'<span class="theme-tags">{" ".join(tags)}</span>' if tags else ''

                # Combine all parts
                entry = f'<li>{authors_str}. {title}. {venue}. {links_str} {tags_str}</li>'
                content += entry

            # Close the last year's list
            if current_year is not None:
                content += "</ol>"

        content += "\n</body>\n</html>"

        return content

    def _verify_browser_setup(self):
        """Verify that the browser is properly set up and can access web pages."""
        try:
            # Try to access a simple page first
            self.driver.get("https://www.google.com")
            time.sleep(2)
            
            if "google" in self.driver.title.lower():
                print("Browser verification successful")
                return True
            else:
                print("Browser verification failed: Unexpected page title")
                return False
        except Exception as e:
            print(f"Browser verification failed: {str(e)}")
            return False

    def update_publications_file(self):
        print("Starting publication update...")
        
        # Verify browser setup
        if not self._verify_browser_setup():
            print("Failed to verify browser setup. Exiting...")
            return False
            
        try:
            publications = self.get_publications()
            if not publications:
                print("No publications were fetched. Exiting...")
                return False
                
            print("Generating markdown content...")
            markdown_content = self.generate_markdown_content(publications)
            
            output_file = 'publications_new.md'
            print(f"Writing to {output_file}...")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"Done! New publications file created at {output_file}")
            return True
            
        except Exception as e:
            print(f"Error updating publications: {str(e)}")
            return False
        finally:
            try:
                self.driver.quit()
            except:
                pass

def load_config():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            return config.get('scholar_id')
    except FileNotFoundError:
        print("Error: config.json not found")
        print("Please create a config.json file with your Google Scholar ID:")
        print('{\n    "scholar_id": "your-scholar-id-here"\n}')
        exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in config.json")
        exit(1)

if __name__ == "__main__":
    # Load Scholar ID from config
    scholar_id = load_config()
    if not scholar_id:
        print("Error: No Scholar ID found in config.json")
        exit(1)
        
    sync = ScholarSync(scholar_id)
    sync.update_publications_file() 
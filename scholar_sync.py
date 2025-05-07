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
        self.scholar_url = f"https://scholar.google.com/citations?user={scholar_id}&hl=en"
        self.crossref_email = "am.das@tue.nl"  # Required by CrossRef for polite API usage
        self._setup_browser()
        self._load_publication_overrides()

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

    def _load_publication_overrides(self):
        """Load publication overrides from JSON file."""
        try:
            with open('publication_overrides.json', 'r') as f:
                self.publication_overrides = json.load(f)
        except FileNotFoundError:
            self.publication_overrides = {}
            print("No publication overrides file found. Using default author lists.")

    def _extract_year_from_scholar_data(self, element):
        """Extract year from Google Scholar citation data."""
        try:
            # Try to find the year in the citation data
            citation_data = element.find_element(By.CLASS_NAME, "gsc_a_y").text
            year_match = re.search(r'\b(19|20)\d{2}\b', citation_data)
            if year_match:
                return int(year_match.group(0))
            
            # If not found in gsc_a_y, try gsc_a_t
            citation_data = element.find_element(By.CLASS_NAME, "gsc_a_t").text
            year_match = re.search(r'\b(19|20)\d{2}\b', citation_data)
            if year_match:
                return int(year_match.group(0))
        except Exception as e:
            print(f"Error extracting year from scholar data: {str(e)}")
        return None

    def _standardize_author_name(self, author: str) -> str:
        """Standardize author name format to always use initials for first and middle names."""
        # Remove any extra spaces
        author = ' '.join(author.split())
        
        # Split into parts
        parts = author.split()
        
        # If it's just one word, return as is
        if len(parts) == 1:
            return author
            
        # If it's two words, convert first name to initial
        if len(parts) == 2:
            return f"{parts[0][0]}. {parts[1]}"
            
        # For three or more words
        if len(parts) >= 3:
            # Convert all but last name to initials
            initials = [part[0] + '.' for part in parts[:-1]]
            return ' '.join(initials + [parts[-1]])
            
        return author

    def _standardize_author_list(self, authors: str) -> str:
        """Standardize a list of author names."""
        author_list = [author.strip() for author in authors.split(',')]
        standardized_authors = [self._standardize_author_name(author) for author in author_list]
        return ', '.join(standardized_authors)

    def _get_publications_from_scholar(self):
        """Get publications from Google Scholar."""
        publications = []
        try:
            # Navigate to Google Scholar profile page
            self.driver.get(self.scholar_url)
            time.sleep(3)  # Wait for page to load
            
            # Click "Show more" button until all publications are loaded
            while True:
                try:
                    show_more = self.driver.find_element(By.ID, "gsc_bpf_more")
                    if not show_more.is_displayed() or not show_more.is_enabled():
                        break
                    show_more.click()
                    time.sleep(2)  # Wait for new publications to load
                except:
                    break
            
            # Now collect all publication links
            pub_links = []
            elements = self.driver.find_elements(By.CLASS_NAME, "gsc_a_tr")
            print(f"Found {len(elements)} publication elements")
            
            for element in elements:
                try:
                    link = element.find_element(By.CLASS_NAME, "gsc_a_at").get_attribute("href")
                    # Get year from the main page first
                    year = self._extract_year_from_scholar_data(element)
                    print(f"Extracted year from main page: {year}")
                    pub_links.append((link, element, year))  # Store link, element, and year
                except Exception as e:
                    print(f"Error getting publication link: {str(e)}")
                    continue

            print(f"Collected {len(pub_links)} publication links")

            # Now process each publication
            for link, element, main_page_year in pub_links:
                try:
                    # Start with the year from main page
                    year = main_page_year
                    
                    # Navigate to publication page
                    self.driver.get(link)
                    time.sleep(2)  # Wait for page to load

                    # Get publication details
                    title = self.driver.find_element(By.CLASS_NAME, "gsc_oci_title_link").text
                    
                    # Check if we have an override for this publication
                    if title in self.publication_overrides:
                        authors = self.publication_overrides[title]['authors']
                    else:
                        authors = self.driver.find_element(By.CLASS_NAME, "gsc_oci_value").text
                    
                    # Standardize author names
                    authors = self._standardize_author_list(authors)
                    
                    venue_elements = self.driver.find_elements(By.CLASS_NAME, "gsc_oci_value")
                    venue = venue_elements[2].text if len(venue_elements) > 2 else ""
                    
                    # Enhanced year extraction if not found on main page
                    if not year:
                        # Try to get year from venue first
                        year_match = re.search(r'\b(19|20)\d{2}\b', venue)
                        if year_match:
                            year = int(year_match.group(0))
                            print(f"Found year in venue: {year}")
                    
                    # If no year in venue, try to get it from the publication page
                    if not year:
                        try:
                            # Look for year in all text elements
                            all_text = self.driver.find_element(By.CLASS_NAME, "gsc_oci_value").text
                            year_match = re.search(r'\b(19|20)\d{2}\b', all_text)
                            if year_match:
                                year = int(year_match.group(0))
                                print(f"Found year in publication page: {year}")
                        except:
                            pass
                    
                    # If still no year, try to get it from the title
                    if not year:
                        year_match = re.search(r'\b(19|20)\d{2}\b', title)
                        if year_match:
                            year = int(year_match.group(0))
                            print(f"Found year in title: {year}")
                    
                    # If still no year, try to get it from the publication date if available
                    if not year:
                        try:
                            date_element = self.driver.find_element(By.CLASS_NAME, "gsc_oci_value")
                            if date_element:
                                date_text = date_element.text
                                year_match = re.search(r'\b(19|20)\d{2}\b', date_text)
                                if year_match:
                                    year = int(year_match.group(0))
                                    print(f"Found year in date: {year}")
                        except:
                            pass
                    
                    # Get DOI if available
                    doi = None
                    try:
                        doi_elements = self.driver.find_elements(By.CLASS_NAME, "gsc_oci_value")
                        for element in doi_elements:
                            if element.text.startswith("10."):
                                doi = element.text
                                break
                    except:
                        pass

                    # Determine category
                    category = "Other Publications"
                    if "thesis" in venue.lower() or "dissertation" in venue.lower():
                        category = "PhD Thesis"
                    elif "arxiv" in venue.lower():
                        category = "Preprints"
                    elif any(journal in venue.lower() for journal in ["journal", "transactions", "letters"]):
                        category = "Journals"
                    else:
                        category = "Conferences"

                    print(f"Found publication: {title} (Category: {category}, Year: {year})")
                    if doi:
                        print(f"  Found DOI: {doi}")

                    # Add publication
                    publications.append({
                        'title': title,
                        'authors': authors,
                        'venue': venue,
                        'year': year,
                        'doi': doi,
                        'category': category,
                        'scholar_link': link
                    })

                    # Go back to main page
                    self.driver.get(self.scholar_url)
                    time.sleep(2)  # Wait for page to load

                except Exception as e:
                    print(f"Error processing publication: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error getting publications from Google Scholar: {str(e)}")
        
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
                    year = pub['year']
                    doi = None
                    
                    # Try to get DOI from CrossRef
                    doi = self.get_doi_from_crossref(title, year=str(year) if year else None, venue=venue)
                    
                    # If no DOI found, try to extract from Google Scholar link
                    if not doi and pub.get('scholar_link'):
                        doi = self.extract_doi_from_scholar_link(pub['scholar_link'])
                    
                    # If still no DOI, try venue-specific patterns
                    if not doi:
                        doi = self.get_doi_from_venue(title, venue, str(year) if year else None)
                    
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
                        'year': year,
                        'doi': doi,
                        'scholar_link': pub.get('scholar_link', '')
                    }
                    
                    # Add category and tags
                    pub_data['category'] = self.classify_publication(pub_data)
                    pub_data['tags'] = self.classify_tags(pub_data)
                    processed_publications.append(pub_data)
                    print(f"Found publication: {title} (Category: {pub_data['category']}, Year: {year})")
                    if doi:
                        print(f"  Found DOI: {doi}")
                    if pub_data['tags']:
                        print(f"  Tags: {', '.join(pub_data['tags'])}")
                    
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

    def classify_tags(self, pub: Dict) -> List[str]:
        """Classify a publication with appropriate tags based on its content."""
        title = pub['title'].lower()
        venue = pub['venue'].lower()
        tags = []

        # PDE-related keywords
        pde_keywords = ['pde', 'partial differential', 'distributed parameter', 'infinite-dimensional', 
                       'spatial', 'spatially varying', 'heat transport', 'mass transport', 'thermal']
        if any(keyword in title or keyword in venue for keyword in pde_keywords):
            tags.append('Control of PDEs')

        # Nonlinear-related keywords
        nonlinear_keywords = ['nonlinear', 'oscillation', 'mixed-feedback', 'lur\'e', 'lur\'e system',
                            'scaled relative graph', 'srg', 'circle criterion']
        if any(keyword in title or keyword in venue for keyword in nonlinear_keywords):
            tags.append('Nonlinear Control')

        # Machine Learning-related keywords
        ml_keywords = ['learning', 'neural', 'data-driven', 'surrogation', 'operator learning', 
                      'gaussian process', 'estimation', 'uncertainty']
        if any(keyword in title or keyword in venue for keyword in ml_keywords):
            tags.append('Machine Learning')

        # Fault-related keywords
        fault_keywords = ['fault', 'diagnosis', 'localisation', 'detection', 'monitoring']
        if any(keyword in title or keyword in venue for keyword in fault_keywords):
            tags.append('Fault Diagnosis')

        return tags

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
    h2 { 
        margin-top: 0; 
        font-size: 1.1em; 
        font-weight: normal; 
        color: #0066cc;  /* Light blue */
        border-bottom: 2px solid #3498db;  /* Bright blue */
        padding-bottom: 5px;
        margin-bottom: 10px;
    }
    h3 { 
        margin-top: 30px; 
        color: #0066cc;  /* Light blue */
        font-size: 1.3em; 
        font-weight: 600;
        border-left: 4px solid #e74c3c;  /* Bright red */
        padding-left: 10px;
    }
    .author-highlight { font-weight: bold; }
    .title-italic { font-style: italic; }
    .venue { color: #597; }  /* Original color */
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
            'Conferences': [],
            'Other Publications': []  # New category for publications without year
        }

        for pub in publications:
            if pub['year'] is None:
                categories['Other Publications'].append(pub)
            else:
                categories[pub['category']].append(pub)

        # Sort publications within each category by year (descending)
        for category in categories:
            if category != 'Other Publications':
                categories[category].sort(key=lambda x: x['year'], reverse=True)
            else:
                # Sort other publications alphabetically by title
                categories[category].sort(key=lambda x: x['title'].lower())

        # Generate content for each category
        for category, pubs in categories.items():
            if not pubs:
                continue

            content += f"\n<h3>{category}</h3>"
            
            if category != 'Other Publications':
                current_year = None
                for pub in pubs:
                    if pub['year'] != current_year:
                        if current_year is not None:
                            content += "</ol>"
                        current_year = pub['year']
                        content += f"\n<h2>{current_year}</h2>\n<ol>"

                    # Format authors
                    authors = pub['authors'].split(', ')
                    # Remove any ellipsis (...) from the author list
                    authors = [author for author in authors if author != '...']
                    authors = [f'<span class="author-highlight">A Das</span>' if 'A Das' in author else author for author in authors]
                    authors_str = ', '.join(authors)

                    # Format title
                    title = f'<span class="title-italic">{pub["title"]}</span>'

                    # Format venue
                    venue = f'<span class="venue">{pub["venue"]}'
                    if category != 'Other Publications' and pub['year']:
                        venue += f', {pub["year"]}'
                    venue += '</span>'

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
            else:
                # Handle Other Publications (no year)
                content += "\n<ol>"
                for pub in pubs:
                    # Format authors
                    authors = pub['authors'].split(', ')
                    # Remove any ellipsis (...) from the author list
                    authors = [author for author in authors if author != '...']
                    authors = [f'<span class="author-highlight">A Das</span>' if 'A Das' in author else author for author in authors]
                    authors_str = ', '.join(authors)

                    # Format title
                    title = f'<span class="title-italic">{pub["title"]}</span>'

                    # Format venue
                    venue = f'<span class="venue">{pub["venue"]}'
                    if category != 'Other Publications' and pub['year']:
                        venue += f', {pub["year"]}'
                    venue += '</span>'

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
                            actual_doi = self.get_doi_from_crossref(pub['title'], venue=pub['venue'])
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

    def update_publications_file(self, direct_update=True):
        """
        Update the publications file.
        
        Args:
            direct_update (bool): If True, directly update publications.md. If False, create publications_new.md
        """
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
            
            if direct_update:
                output_file = 'publications.md'
                backup_file = 'publications.md.backup'
                print(f"Creating backup at {backup_file}...")
                try:
                    # Create backup of existing file
                    if os.path.exists(output_file):
                        import shutil
                        shutil.copy2(output_file, backup_file)
                except Exception as e:
                    print(f"Warning: Could not create backup: {str(e)}")
            else:
                output_file = 'publications_new.md'
            
            print(f"Writing to {output_file}...")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            if direct_update:
                print(f"Done! Publications file updated at {output_file}")
                print(f"Backup created at {backup_file}")
            else:
                print(f"Done! New publications file created at {output_file}")
                print("Please review the new file and rename it to publications.md if everything looks correct")
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
    # Direct update is now the default behavior
    sync.update_publications_file() 
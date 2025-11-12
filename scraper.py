"""
Modul untuk web scraping abstrak dari ejournal.unesa.ac.id
"""
import requests
from bs4 import BeautifulSoup
import time
import re
from typing import List, Dict
from models import db, Abstract


class JournalScraper:
    """Class untuk scraping data dari ejournal UNESA"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_articles_by_year(self, year: int) -> List[Dict]:
        """
        Scrape artikel berdasarkan tahun tertentu
        """
        articles = []
        
        try:
            # URL untuk archive berdasarkan tahun
            archive_url = f"{self.base_url}/issue/archive"
            print(f"📥 Fetching archive: {archive_url}")
            response = self.session.get(archive_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cari semua link issue yang mengandung tahun yang dicari
            # Format: "Volume XX No X YYYY"
            all_links = soup.find_all('a', href=lambda x: x and '/issue/view/' in x)
            
            issue_urls = []
            for link in all_links:
                link_text = link.text.strip()
                link_year = self._extract_year(link_text)
                
                if link_year == year:
                    issue_url = link.get('href')
                    if issue_url not in issue_urls:
                        issue_urls.append(issue_url)
                        print(f"   ✓ Found: {link_text}")
            
            print(f"📚 Total {len(issue_urls)} issue(s) found for year {year}")
            
            # Scrape setiap issue
            for i, issue_url in enumerate(issue_urls, 1):
                print(f"\n   [{i}/{len(issue_urls)}] Scraping issue: {issue_url}")
                issue_articles = self._scrape_issue(issue_url)
                articles.extend(issue_articles)
                print(f"   ✓ Got {len(issue_articles)} article(s) from this issue")
                time.sleep(2)  # Delay untuk menghindari rate limiting
            
        except Exception as e:
            print(f"❌ Error scraping year {year}: {str(e)}")
        
        return articles
    
    def _scrape_issue(self, issue_url: str) -> List[Dict]:
        """
        Scrape semua artikel dari satu issue
        """
        articles = []
        
        try:
            response = self.session.get(issue_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cari semua artikel dalam issue
            article_summaries = soup.find_all('div', class_='obj_article_summary')
            
            print(f"      → Found {len(article_summaries)} article(s) in this issue")
            
            for idx, article_summary in enumerate(article_summaries, 1):
                # Cari link artikel (bisa di berbagai elemen)
                article_link = article_summary.find('a', href=lambda x: x and '/article/view/' in x)
                
                if article_link:
                    article_url = article_link.get('href')
                    article_title = article_link.text.strip()[:50]
                    print(f"         [{idx}/{len(article_summaries)}] {article_title}...")
                    
                    article_data = self._scrape_article(article_url)
                    if article_data:
                        articles.append(article_data)
                        print(f"         ✓ Success")
                    else:
                        print(f"         ⚠ No abstract found")
                    time.sleep(1)  # Delay antar artikel
        
        except Exception as e:
            print(f"      ❌ Error scraping issue {issue_url}: {str(e)}")
        
        return articles
    
    def _scrape_article(self, article_url: str) -> Dict:
        """
        Scrape detail artikel (judul, penulis, tahun, abstrak)
        """
        try:
            response = self.session.get(article_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract judul - coba berbagai selector
            title = ''
            title_elem = soup.find('h1', class_='page_title')
            if not title_elem:
                title_elem = soup.find('h1', class_='title')
            if not title_elem:
                title_elem = soup.find('h1')
            if title_elem:
                title = title_elem.text.strip()
            
            # Extract penulis
            authors = []
            author_elems = soup.find_all('span', class_='name')
            if not author_elems:
                author_elems = soup.find_all('a', class_='author')
            for author_elem in author_elems:
                authors.append(author_elem.text.strip())
            author = ', '.join(authors) if authors else 'Unknown'
            
            # Extract tahun dari published date
            year = 0
            published_elem = soup.find('div', class_='published')
            if published_elem:
                year = self._extract_year(published_elem.text)
            
            # Jika tidak ada tahun, cari di metadata lain
            if year == 0:
                # Cari di breadcrumb atau title
                year = self._extract_year(title)
            
            # Extract abstrak - coba berbagai selector
            abstract_text = ''
            
            # Method 1: section.item.abstract
            abstract_section = soup.find('section', class_='item abstract')
            
            # Method 2: div.abstract
            if not abstract_section:
                abstract_section = soup.find('div', class_='abstract')
            
            # Method 3: Cari heading "Abstract" atau "Abstrak"
            if not abstract_section:
                headings = soup.find_all(['h2', 'h3', 'h4'])
                for heading in headings:
                    if 'abstract' in heading.text.lower() or 'abstrak' in heading.text.lower():
                        # Ambil sibling paragraf
                        next_elem = heading.find_next_sibling()
                        if next_elem and next_elem.name == 'p':
                            abstract_text = next_elem.text.strip()
                        break
            
            if abstract_section and not abstract_text:
                # Ambil semua teks dari section, kecuali heading
                for elem in abstract_section.find_all(['h2', 'h3', 'h4', 'strong']):
                    elem.decompose()  # Hapus heading
                
                # Ambil teks dari paragraf
                paragraphs = abstract_section.find_all('p')
                if paragraphs:
                    abstract_text = ' '.join([p.text.strip() for p in paragraphs])
                else:
                    # Jika tidak ada <p>, ambil semua teks
                    abstract_text = abstract_section.get_text(strip=True)
            
            # Bersihkan teks
            abstract_text = self._clean_text(abstract_text)
            
            # Hapus kata "Abstract" atau "Abstrak" di awal
            abstract_text = re.sub(r'^(abstract|abstrak)[:\s]*', '', abstract_text, flags=re.IGNORECASE).strip()
            
            if title and abstract_text:
                return {
                    'title': title,
                    'author': author,
                    'year': year,
                    'abstract_text': abstract_text,
                    'url': article_url
                }
        
        except Exception as e:
            print(f"Error scraping article {article_url}: {str(e)}")
        
        return None
    
    def _extract_year(self, text: str) -> int:
        """Extract tahun dari teks"""
        year_match = re.search(r'20[12][0-9]', text)
        return int(year_match.group()) if year_match else 0
    
    def _clean_text(self, text: str) -> str:
        """Bersihkan teks dari karakter yang tidak perlu"""
        # Hapus multiple whitespace
        text = re.sub(r'\s+', ' ', text)
        # Hapus karakter khusus berlebihan
        text = re.sub(r'\n+', ' ', text)
        return text.strip()
    
    def scrape_range(self, start_year: int, end_year: int) -> List[Dict]:
        """
        Scrape artikel dari rentang tahun tertentu
        """
        all_articles = []
        
        for year in range(start_year, end_year + 1):
            print(f"Scraping year {year}...")
            articles = self.get_articles_by_year(year)
            all_articles.extend(articles)
            print(f"Found {len(articles)} articles in {year}")
            time.sleep(3)  # Delay antar tahun
        
        return all_articles
    
    def save_to_database(self, articles: List[Dict]) -> int:
        """
        Simpan artikel ke database
        Returns: jumlah artikel yang berhasil disimpan
        """
        saved_count = 0
        
        for article_data in articles:
            try:
                # Cek apakah artikel sudah ada (berdasarkan judul dan tahun)
                existing = Abstract.query.filter_by(
                    title=article_data['title'],
                    year=article_data['year']
                ).first()
                
                if not existing:
                    abstract = Abstract(
                        title=article_data['title'],
                        author=article_data['author'],
                        year=article_data['year'],
                        abstract_text=article_data['abstract_text'],
                        url=article_data.get('url', '')
                    )
                    db.session.add(abstract)
                    saved_count += 1
            
            except Exception as e:
                print(f"Error saving article: {str(e)}")
                continue
        
        try:
            db.session.commit()
            print(f"Successfully saved {saved_count} articles to database")
        except Exception as e:
            db.session.rollback()
            print(f"Error committing to database: {str(e)}")
            return 0
        
        return saved_count


def scrape_and_save(base_url: str, start_year: int, end_year: int, auto_label=True):
    """
    Fungsi helper untuk scraping dan menyimpan ke database
    
    Args:
        base_url: URL dasar journal
        start_year: Tahun mulai scraping
        end_year: Tahun akhir scraping
        auto_label: Jika True (default), otomatis label data hasil scraping menggunakan keyword scoring
    """
    from auto_labeler import auto_label_text
    
    scraper = JournalScraper(base_url)
    articles = scraper.scrape_range(start_year, end_year)
    
    if articles:
        saved = scraper.save_to_database(articles)
        
        result = {
            'total_scraped': len(articles),
            'total_saved': saved,
            'message': f'Successfully scraped {len(articles)} articles, saved {saved} new articles'
        }
        
        # Auto-label menggunakan keyword-based scoring (SELALU aktif untuk data scraping)
        if auto_label and saved > 0:
            try:
                # Ambil artikel yang baru saja disimpan (belum ada label)
                new_abstracts = Abstract.query.filter(
                    Abstract.label.is_(None),
                    Abstract.predicted_label.is_(None)
                ).all()
                
                if new_abstracts:
                    print(f"\n🤖 Auto-labeling {len(new_abstracts)} new articles using keyword scoring...")
                    
                    # Label menggunakan keyword-based auto-labeler
                    rpl_count = 0
                    tkj_count = 0
                    
                    for abstract in new_abstracts:
                        label, confidence = auto_label_text(abstract.abstract_text)
                        
                        # Set sebagai label (bukan predicted_label) karena ini data training
                        # User bisa koreksi manual di halaman /label jika perlu
                        abstract.label = label
                        abstract.confidence = confidence
                        
                        if label == 'RPL':
                            rpl_count += 1
                        else:
                            tkj_count += 1
                    
                    db.session.commit()
                    
                    result['auto_labeled'] = len(new_abstracts)
                    result['rpl_count'] = rpl_count
                    result['tkj_count'] = tkj_count
                    result['message'] += f' | Auto-labeled: {len(new_abstracts)} (RPL: {rpl_count}, TKJ: {tkj_count})'
                    
                    print(f"✓ Auto-labeling complete! RPL: {rpl_count}, TKJ: {tkj_count}")
                    
            except Exception as e:
                print(f"❌ Error during auto-labeling: {str(e)}")
                result['auto_label_error'] = str(e)
        
        return result
    else:
        return {
            'total_scraped': 0,
            'total_saved': 0,
            'message': 'No articles found'
        }

import time
import random
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MubawabScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def get_page(self, url, max_retries=3):
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                logger.warning(f"Erreur lors de la récupération de {url} (tentative {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(random.uniform(2, 5))
                else:
                    logger.error(f"Échec définitif pour {url}")
                    return None
        return None

    def extract_description_between_title_and_marker(self, soup, title):
        full_text = soup.get_text(separator=" ", strip=True)
        full_text_clean = full_text.replace('\xa0', ' ').strip()
        title_clean = title.replace('\xa0', ' ').strip()
        end_marker = "Caractéristiques générales"

        end_index = full_text_clean.lower().find(end_marker.lower())
        if end_index == -1:
            return None

        search_area = full_text_clean[:end_index]
        start_index = search_area.lower().rfind(title_clean.lower())
        if start_index == -1:
            return None

        description = full_text_clean[start_index + len(title_clean):end_index].strip()
        return description if description else None

    def get_listing_details(self, detail_url):
        try:
            response = self.get_page(detail_url)
            if not response:
                return None, None, None, None, None

            soup = BeautifulSoup(response.text, 'html.parser')

            property_type = None
            size = None
            rooms = None
            description = None
            image_urls = []

            # Récupérer le vrai titre affiché dans la page HTML
            real_title = None
            title_selectors = [
                '.listingTit',
                'h1',
                'h2',
                '[class*="title"]'
            ]
            for selector in title_selectors:
                title_element = soup.select_one(selector)
                if title_element:
                    real_title = title_element.get_text(strip=True)
                    break

            # Utiliser ce titre pour extraire la description
            if real_title:
                description = self.extract_description_between_title_and_marker(soup, real_title)
                if not description:
                    logger.warning(f"Aucune description extraite avec le vrai titre pour {detail_url}")
            else:
                logger.warning(f"Titre non trouvé dans la page HTML pour {detail_url}")

            # Recherche des images
            image_selectors = [
                '.adPictures img',
                '.gallery img',
                '[class*="photo"] img',
                '.photo-gallery img'
            ]
            for selector in image_selectors:
                images = soup.select(selector)
                for img in images:
                    img_url = img.get('src') or img.get('data-src')
                    if img_url:
                        full_url = urljoin('https://www.mubawab.ma', img_url)
                        if full_url not in image_urls:
                            image_urls.append(full_url)

            # Type de propriété
            type_selectors = [
                'span.adMainFeatureContentValue',
                'p.adMainFeatureContentValue',
                '.adMainFeatureContentValue',
                '[class*="feature"] [class*="value"]'
            ]
            for selector in type_selectors:
                element = soup.select_one(selector)
                if element:
                    property_type = element.get_text(strip=True)
                    break

            # Taille et chambres
            size_selectors = [
                '.adDetails span',
                '.disFlex.adDetails span',
                '[class*="details"] span',
                '.property-details span'
            ]
            for selector in size_selectors:
                elements = soup.select(selector)
                if len(elements) >= 2:
                    size = elements[0].get_text(strip=True)
                    rooms = elements[1].get_text(strip=True)
                    break

            if not size or not rooms:
                feature_items = soup.select('[class*="feature"], [class*="detail"], .adMainFeature')
                for item in feature_items:
                    text = item.get_text(strip=True)
                    if 'm²' in text and not size:
                        size = text
                    elif ('chambre' in text.lower() or 'pièce' in text.lower()) and not rooms:
                        rooms = text

            return property_type, size, rooms, description, image_urls

        except Exception as e:
            logger.error(f"Erreur lors de la récupération des détails de {detail_url}: {e}")
            return None, None, None, None, None

    def scrape_page(self, page_number):
        base_url = f'https://www.mubawab.ma/fr/sc/immobilier-divers-a-louer:p:{page_number}'
        response = self.get_page(base_url)
        if not response:
            logger.error(f"Impossible de récupérer la page {page_number}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')

        listing_selectors = [
            'li.listingBox',
            'li[class*="listing"]',
            '.listingBox',
            '[class*="listing-item"]'
        ]
        listings = []
        for selector in listing_selectors:
            listings = soup.select(selector)
            if listings:
                break

        logger.info(f"Trouvé {len(listings)} annonces sur la page {page_number}")

        data = []
        for i, listing in enumerate(listings, 1):
            try:
                logger.info(f"Traitement de l'annonce {i}/{len(listings)}")

                posting_url = None
                url_selectors = ['a[href]', '[href*="/ad/"]']
                for selector in url_selectors:
                    link = listing.select_one(selector)
                    if link and link.get('href'):
                        posting_url = urljoin('https://www.mubawab.ma', link['href'])
                        break

                price = None
                price_selectors = [
                    '.priceTag',
                    '[class*="price"]',
                    '.price-value',
                    'span[class*="price"]'
                ]
                for selector in price_selectors:
                    price_element = listing.select_one(selector)
                    if price_element:
                        price = price_element.get_text(strip=True)
                        break

                neighbourhood = None
                neighbourhood_selectors = [
                    '.listingH3',
                    'h3',
                    '[class*="location"]',
                    '.location'
                ]
                for selector in neighbourhood_selectors:
                    neighbourhood_element = listing.select_one(selector)
                    if neighbourhood_element:
                        neighbourhood = neighbourhood_element.get_text(strip=True)
                        break

                image_url = None
                image_selectors = [
                    '.photoBox',
                    'img[src]',
                    '[class*="photo"] img',
                    '[data-url]'
                ]
                for selector in image_selectors:
                    image_element = listing.select_one(selector)
                    if image_element:
                        image_url = image_element.get('data-url') or image_element.get('src')
                        if image_url:
                            image_url = urljoin('https://www.mubawab.ma', image_url)
                        break

                title = None
                title_selectors = [
                    '.listingTit',
                    'h2',
                    '[class*="title"]',
                    '.title'
                ]
                for selector in title_selectors:
                    title_element = listing.select_one(selector)
                    if title_element:
                        title = title_element.get_text(strip=True)
                        break

                property_type, size, rooms, description, all_images = None, None, None, None, None
                if posting_url:
                    logger.info(f"Récupération des détails pour: {posting_url}")
                    property_type, size, rooms, description, all_images = self.get_listing_details(posting_url)
                    time.sleep(random.uniform(1, 3))

                data.append({
                    'Title': title,
                    'Price': price,
                    'Neighbourhood': neighbourhood,
                    'All Images': ', '.join(all_images) if all_images else None,
                    'Description': description,
                    'Posting URL': posting_url,
                    'Property Type': property_type,
                    'Size': size,
                    'Rooms': rooms
                })

                logger.info(f"Annonce scrapée: {title}")

            except Exception as e:
                logger.error(f"Erreur lors du traitement de l'annonce {i}: {e}")
                time.sleep(random.uniform(1, 2))

        return data

    def scrape_all_pages(self, total_pages=1):
        all_data = []
        for page_number in range(1, total_pages + 1):
            logger.info(f"Début du scraping de la page {page_number}")
            page_data = self.scrape_page(page_number)
            if page_data:
                all_data.extend(page_data)
                logger.info(f"Page {page_number} terminée - {len(page_data)} annonces récupérées")
            else:
                logger.warning(f"Aucune donnée récupérée pour la page {page_number}")
            if page_number < total_pages:
                delay = random.uniform(2, 5)
                logger.info(f"Attente de {delay:.1f} secondes avant la page suivante")
                time.sleep(delay)

        if all_data:
            df = pd.DataFrame(all_data)
            filename = f'mubawab_locations_{int(time.time())}.csv'
            df.to_csv(filename, index=False, encoding='utf-8')
            logger.info(f'Données sauvegardées dans {filename}')
            logger.info(f'Total: {len(all_data)} annonces récupérées')
        else:
            logger.warning("Aucune donnée à sauvegarder")

        return all_data

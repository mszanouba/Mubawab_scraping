import mubawab_scraping.mubawab_scraper as ms

if __name__ == "__main__":
    scraper = ms.MubawabScraper()
    scraper.scrape_all_pages(total_pages=1)


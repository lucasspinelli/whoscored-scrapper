
class WebScraperManager:
    def __init__(self):
        self.configs = []

    def add_config(self, scraper_class, url, directory, file_name_pattern):
        self.configs.append({
            "scraper_class": scraper_class,
            "url": url,
            "directory": directory,
            "file_name_pattern": file_name_pattern
        })

    def run_scrapers(self):
        for config in self.configs:
            scraper = config["scraper_class"](config["url"], config["directory"], config["file_name_pattern"])
            scraper.scrape()
            print(f"Completed scraping: {config['url']} saved to {config['directory']}/{config['file_name_pattern']}.csv")

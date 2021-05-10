from data_collector_main import WebsiteDataCollector

collector = WebsiteDataCollector(
                "Fool_collector",
                "https://www.fool.com",
                "https://www.fool.com/investing-news/?page=9999")

collector.crawl()

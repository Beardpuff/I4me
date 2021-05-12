from fool_collector import FoolCollector

collector = FoolCollector(
                "Fool_collector",
                "https://www.fool.com",
                range(0, 10))

collector.crawl(verbose=True)

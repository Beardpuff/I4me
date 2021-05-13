from fool_collector import FoolCollector

collector = FoolCollector(
                "Fool_collector",
                "https://www.fool.com",
                range(0, 1),
                initial_has_info=True,
                initial_address=["https://www.fool.com/investing/2021/04/10/could-astrazenecas-nasal-covid-vaccine-development/",
                                 "https://www.fool.com/investing/2021/04/10/the-secret-to-legally-pay-zero-taxes-on-bitcoin-pr/",
                                 "https://www.fool.com/investing/2021/04/10/1-great-stock-you-can-buy-on-sale-right-now/",
                                 "https://www.fool.com/investing/2021/04/17/novavax-is-missing-out-on-a-big-deal/"])

collector.crawl(depth=0, verbose=True)

# collector = FoolCollector(
#                 "fool_collector",
#                 "https://www.fool.com",
#                 range(100, 200))

# collector.crawl(verbose=True)

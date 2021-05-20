from fool_collector import FoolCollector
import time

# collector = FoolCollector(
#                 "Fool_collector",
#                 "https://www.fool.com",
#                 range(0, 1),
#                 initial_has_info=True,
#                 initial_address=["https://www.fool.com/retirement/2021/05/16/3-social-security-decisions-that-could-haunt-you-f/"])#,
#                                  # "https://www.fool.com/the-ascent/personal-finance/articles/stimulus-check-update-165-million-payments-sent-to-date/",
#                                  # "https://www.fool.com/investing/general/2010/11/30/has-western-refining-made-you-any-real-money.aspx",
#                                  # "https://www.fool.com/investing/2021/05/13/ping-identity-can-finally-compete-with-okta/",
#                                  # "https://www.fool.com/investing/2021/05/13/why-ill-never-sell-my-netflix-stock/",
#                                  # "https://www.fool.com/investing/2021/05/13/where-to-invest-5000-right-now/",
#                                  # "https://www.fool.com/investing/2021/04/10/could-astrazenecas-nasal-covid-vaccine-development/",
#                                  # "https://www.fool.com/investing/2021/04/10/1-great-stock-you-can-buy-on-sale-right-now/",
#                                  # "https://www.fool.com/investing/2021/04/10/the-secret-to-legally-pay-zero-taxes-on-bitcoin-pr/",
#                                  # "https://www.fool.com/investing/2021/04/17/novavax-is-missing-out-on-a-big-deal/"])

# collector.crawl(depth=0, verbose=True)

# =================================================================

collector = FoolCollector(
                "fool_collector",
                "https://www.fool.com",
                range(20, 0, -1)) # range(24000, 23900, -1))

start_time = time.time()
collector.crawl(verbose=True)
print("Crawl Completed in {:f} seconds!".format(time.time() - start_time))

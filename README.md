# Goal

EquityZen sources investments in pre-ipo companies. However, it's email notifications for express investments dont always work. Instead of manually opening tabs for all the companies on my watchlist, I created this scraper to get a quick summary of investment opportunities.

The output of `./eqzscrape.sh` looks like this

```
-- ALL AVAILABLE --
Offer(company='nextdoor', date='2021-06-30', underlying_share_class='Common Stock', implied_share_price='$53.00', implied_valuation='$6.4B', investment_size='$32,171.00', days_posted='1')
Offer(company='nextdoor', date='2021-06-30', underlying_share_class='Common Stock', implied_share_price='$69.00', implied_valuation='$8.3B', investment_size='$41,883.00', days_posted='16')

-- Insertions --
Offer(company='nextdoor', date='2021-06-30', underlying_share_class='Common Stock', implied_share_price='$53.00', implied_valuation='$6.4B', investment_size='$32,171.00', days_posted='1')

-- Deletions --

```

# Requirements

This package uses node, npm, and python3.7. I also need the puppeteer npm package.

# Performance

This package took <1m to scrape 12 companies. I am opening urls sequentially in puppeteer, and that can be parallelized for heavier work but for my personal work this was enough.

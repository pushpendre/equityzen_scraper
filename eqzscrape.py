from pdb import set_trace as st
import argparse, dataclasses, re, pprint, json
from typing import List
OFFSET = len('https://equityzen.com/company/')

def iterator(scrape_stdout_filename: str):
    L = []
    for row in open(scrape_stdout_filename):
        if row != '\n':
            L.append(row.strip())
        else:
            assert len(L) == 2
            yield L
            L.clear()
    if L:
        assert len(L) == 2
        yield L
    return

@dataclasses.dataclass
class Offer:
    company: str
    date: str
    underlying_share_class: str
    implied_share_price: float
    implied_valuation: str
    investment_size: int
    days_posted: int

    def custom_hash(self):
        return (self.company, self.implied_valuation, self.investment_size)


def parse(inner_html: str, company: str, date: str) -> List[Offer]:
    tmp = [re.findall('>([^>]+)</td>', row)
           for row
           in inner_html.split('</tr>')
           if row != '']
    return [Offer(company, date, *e) for e in tmp]

def main(args):
    old_offers, old_hashes = [], []
    try:
        old_offers = [Offer(**e) for e in json.load(open(args.storage))]
        old_hashes = {e.custom_hash() for e in old_offers}
    except FileNotFoundError:
        pass

    new_offers = [
        offer
        for url, offer in iterator(args.scrape_stdout)
        if offer != 'undefined'
        for offer in parse(offer, url[OFFSET: -1], args.sfx)]
    new_hashes = {e.custom_hash() for e in new_offers}

    insertions = [e for e in new_offers if e.custom_hash() not in old_hashes]
    deletions = [e for e in old_offers if e.custom_hash() not in new_hashes]

    print('-- ALL AVAILABLE --')
    for e in new_offers:
        pprint.pprint(e)
    print()
    print('-- Insertions --')
    for e in insertions:
        pprint.pprint(e)
    print()
    print('-- Deletions --')
    for e in deletions:
        pprint.pprint(e)

    with open(args.storage, 'w') as f:
        json.dump([dataclasses.asdict(e) for e in new_offers], f, indent=4)

    return

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('scrape_stdout')
    arg_parser.add_argument('scrape_stderr')
    arg_parser.add_argument('sfx')
    arg_parser.add_argument('--storage', default='eqzscrape.json')
    main(arg_parser.parse_args())

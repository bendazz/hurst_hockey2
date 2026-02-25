#!/usr/bin/env python3
import re
import csv
import html
from urllib.request import urlopen, Request

URL = 'https://hurstathletics.com/sports/mens-ice-hockey/stats/2025-26'

def fetch(url):
    req = Request(url, headers={'User-Agent': 'python-urllib'})
    return urlopen(req).read().decode('utf-8', errors='ignore')

def extract_section_table(html_text):
    # Find the Individual Overall Skaters section and its first table
    m = re.search(r'<section[^>]+id="individual-overall-skaters"[\s\S]*?<table[^>]*>([\s\S]*?)</table>', html_text, re.I)
    return m.group(1) if m else ''

def strip_tags(text):
    return re.sub(r'<[^>]+>', '', text).strip()

def parse_rows(table_html):
    # Find tbody and its trs
    tbody_m = re.search(r'<tbody[^>]*>([\s\S]*?)</tbody>', table_html, re.I)
    if not tbody_m:
        return []
    tbody = tbody_m.group(1)
    rows = re.findall(r'<tr[^>]*>([\s\S]*?)</tr>', tbody, re.I)
    parsed = []
    for tr in rows:
        # extract all td contents in order
        tds = re.findall(r'<td[^>]*>([\s\S]*?)</td>', tr, re.I)
        if not tds:
            continue
        # First td is the number; second is player (may contain <a> and <span>)
        num = strip_tags(tds[0])
        player = strip_tags(tds[1])
        # remaining tds are the numeric/stat columns; keep text, collapse whitespace
        cols = [re.sub(r'\s+', ' ', strip_tags(td)) for td in tds[2:]]
        # Some rows may include an extra final td for bio; ignore if present beyond expected
        # Expected columns after player: GP,G,A,PTS,SH,SH%,+/-,PPG,SHG,FG,GWG,GTG,OTG,HTG,UAG,PN-PIM,MIN,MAJ,OTH,BLK
        expected_after_player = 20
        if len(cols) < expected_after_player:
            # skip malformed rows
            continue
        cols = cols[:expected_after_player]
        parsed.append([num, player] + cols)
    return parsed

def main():
    src = fetch(URL)
    table_html = extract_section_table(src)
    rows = parse_rows(table_html)
    out_path = 'stats.csv'
    header = [h.strip() for h in '#,Player,GP,G,A,PTS,SH,SH%,+/- ,PPG,SHG,FG,GWG,GTG,OTG,HTG,UAG,PN-PIM,MIN,MAJ,OTH,BLK'.split(',')]
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            # unescape HTML entities
            row = [html.unescape(cell) for cell in r]
            w.writerow(row)
    print(f'Wrote {len(rows)} rows to {out_path}')

if __name__ == '__main__':
    main()

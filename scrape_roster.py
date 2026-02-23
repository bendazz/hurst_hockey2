#!/usr/bin/env python3
"""Scrape Hurst men's hockey roster and write players.csv"""
import csv
import sys
import requests
from bs4 import BeautifulSoup

ROSTER_URL = "https://hurstathletics.com/sports/mens-ice-hockey/roster"

def fetch(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    resp = requests.get(url, timeout=20, headers=headers)
    resp.raise_for_status()
    return resp.text

def extract_player_urls(roster_html):
    import re
    matches = re.findall(r'(?:https?://[\w\.-]+)?/roster\.aspx\?rp_id=\d+', roster_html)
    urls = set()
    for m in matches:
        if m.startswith('http'):
            urls.add(m)
        else:
            urls.add('https://hurstathletics.com' + m)
    return sorted(urls)

def parse_player(html):
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find('div', class_='sidearm-roster-player-header-details')
    if not div:
        return None

    num_tag = div.find('span', class_='sidearm-roster-player-jersey-number')
    number = num_tag.get_text(strip=True) if num_tag else ""

    name_tag = div.find('span', class_='sidearm-roster-player-name')
    first = last = ""
    if name_tag:
        spans = name_tag.find_all('span')
        if len(spans) >= 1:
            first = spans[0].get_text(strip=True)
        if len(spans) >= 2:
            last = spans[1].get_text(strip=True)

    field_map = {}
    for dt in div.find_all('dt'):
        label = dt.get_text(strip=True).rstrip(':')
        dd = dt.find_next_sibling('dd')
        value = dd.get_text(strip=True) if dd else ""
        field_map[label] = value

    return {
        'Position': field_map.get('Position', ''),
        'Weight': field_map.get('Weight', ''),
        'Height': field_map.get('Height', ''),
        'Hometown': field_map.get('Hometown', ''),
        'Class': field_map.get('Class', ''),
        'High School': field_map.get('High School', ''),
        'Number': number,
        'First Name': first,
        'Last Name': last,
    }

def write_csv(players, path='players.csv'):
    fieldnames = ['Position','Weight','Height','Hometown','Class','High School','Number','First Name','Last Name']
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in players:
            writer.writerow(p)

def main():
    try:
        roster_html = fetch(ROSTER_URL)
    except Exception as e:
        print('Failed to fetch roster page:', e, file=sys.stderr)
        sys.exit(1)

    urls = extract_player_urls(roster_html)
    players = []
    for u in urls:
        try:
            html = fetch(u)
        except Exception as e:
            print(f'Warning: failed to fetch {u}: {e}', file=sys.stderr)
            continue
        p = parse_player(html)
        if p:
            players.append(p)

    write_csv(players)
    print(f'Wrote {len(players)} players to players.csv')

if __name__ == '__main__':
    main()

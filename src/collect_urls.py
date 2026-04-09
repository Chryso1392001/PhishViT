"""
PhishViT — URL Collection Script
Author: Jean Chrysostome NDAYISABYE
University of Rwanda, Department of Information Systems
"""

import requests
import pandas as pd
import os
import zipfile
import io

RAW_DIR = os.path.expanduser("~/phishvit/data/raw")
os.makedirs(RAW_DIR, exist_ok=True)

def collect_phishing(limit=300):
    """Collect phishing URLs from OpenPhish community feed."""
    print("Collecting phishing URLs from OpenPhish...")
    try:
        response = requests.get("https://openphish.com/feed.txt", timeout=30)
        urls = [u.strip() for u in response.text.strip().split('\n') if u.strip()]
        urls = list(set(urls))[:limit]
        df = pd.DataFrame({'url': urls, 'label': 1})
        out = os.path.join(RAW_DIR, "phishing_urls.csv")
        df.to_csv(out, index=False)
        print(f"✅ Saved {len(df)} phishing URLs → {out}")
        return df
    except Exception as e:
        print(f"⚠️  OpenPhish failed: {e}")
        return pd.DataFrame()

def collect_legitimate(limit=300):
    """Collect legitimate URLs from Tranco Top-1M list."""
    print("Collecting legitimate URLs from Tranco...")
    try:
        response = requests.get(
            "https://tranco-list.eu/top-1m.csv.zip",
            timeout=60, stream=True)
        content = b""
        total = 0
        for chunk in response.iter_content(chunk_size=8192):
            content += chunk
            total += len(chunk)
            if total % (1024*1024) == 0:
                print(f"  Downloaded {total//(1024*1024)}MB...", end='\r')
        z = zipfile.ZipFile(io.BytesIO(content))
        with z.open(z.namelist()[0]) as f:
            df = pd.read_csv(f, header=None, names=['rank', 'domain'])
        df = df.iloc[:limit]
        df['url'] = 'https://' + df['domain']
        legit_df = df[['url']].copy()
        legit_df['label'] = 0
        out = os.path.join(RAW_DIR, "legitimate_urls.csv")
        legit_df.to_csv(out, index=False)
        print(f"\n✅ Saved {len(legit_df)} legitimate URLs → {out}")
        return legit_df
    except Exception as e:
        print(f"\n⚠️  Tranco failed: {e}")
        return pd.DataFrame()

def merge_urls():
    """Merge all collected URL files into master CSV."""
    print("\nMerging URL files...")
    all_dfs = []
    for fname in os.listdir(RAW_DIR):
        if fname.endswith('.csv') and 'urls' in fname and 'master' not in fname:
            path = os.path.join(RAW_DIR, fname)
            df = pd.read_csv(path)
            if 'url' in df.columns and 'label' in df.columns:
                all_dfs.append(df)
                print(f"  Loaded {fname}: {len(df)} URLs")

    if not all_dfs:
        print("⚠️  No URL files found!")
        return pd.DataFrame()

    master = pd.concat(all_dfs, ignore_index=True)
    master = master.drop_duplicates(subset=['url'])
    master = master.sample(frac=1, random_state=42).reset_index(drop=True)
    out = os.path.join(RAW_DIR, "master_urls.csv")
    master.to_csv(out, index=False)

    print(f"\n✅ Master CSV saved → {out}")
    print(f"📊 Total   : {len(master)}")
    print(f"🎣 Phishing: {len(master[master.label==1])}")
    print(f"✅ Legit   : {len(master[master.label==0])}")
    return master

if __name__ == "__main__":
    collect_phishing(limit=300)
    collect_legitimate(limit=300)
    merge_urls()
    print("\n✅ Done! Next: run screenshot_capture_v2.py")

"""
PhishViT — Screenshot Capture Pipeline V2
Author: Jean Chrysostome NDAYISABYE
University of Rwanda, Department of Information Systems

Usage:
    python screenshot_capture_v2.py

Requirements:
    pip install playwright pandas tqdm
    playwright install chromium
"""

import asyncio
import pandas as pd
import os
from playwright.async_api import async_playwright
from tqdm import tqdm
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────
RAW_DIR   = os.path.expanduser("~/phishvit/data/raw")
PHISH_DIR = os.path.expanduser("~/phishvit/data/phishing")
LEGIT_DIR = os.path.expanduser("~/phishvit/data/legitimate")

os.makedirs(PHISH_DIR, exist_ok=True)
os.makedirs(LEGIT_DIR, exist_ok=True)

# ── Config ─────────────────────────────────────────────────────
TIMEOUT     = 15000   # 15 seconds navigation timeout
WAIT_MS     = 2000    # 2 seconds post-load wait
MAX_SAMPLES = 300     # max per class
VIEWPORT    = {"width": 1280, "height": 800}


async def capture_screenshot(page, url: str, save_path: str) -> bool:
    """Capture a screenshot of the given URL."""
    try:
        await page.goto(url, timeout=TIMEOUT, wait_until="domcontentloaded")
        await asyncio.sleep(WAIT_MS / 1000)
        await page.screenshot(path=save_path, full_page=False)
        return True
    except Exception:
        return False


async def main():
    # Load master URLs
    master_path = os.path.join(RAW_DIR, "master_urls.csv")
    if not os.path.exists(master_path):
        print(f"❌ master_urls.csv not found at {master_path}")
        print("   Run collect_urls.py first!")
        return

    df = pd.read_csv(master_path)
    phish_df = df[df['label'] == 1].reset_index(drop=True)
    legit_df = df[df['label'] == 0].head(MAX_SAMPLES).reset_index(drop=True)

    # Get already captured screenshots
    existing_phish = set(os.listdir(PHISH_DIR))
    existing_legit = set(os.listdir(LEGIT_DIR))

    print("=" * 55)
    print(f"  PhishViT Screenshot Capture V2")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 55)
    print(f"  🎣 Phishing URLs  : {len(phish_df)}")
    print(f"  ✅ Legitimate URLs: {len(legit_df)}")
    print(f"  📸 Already captured:")
    print(f"     Phishing  : {len(existing_phish)}")
    print(f"     Legitimate: {len(existing_legit)}")
    print("=" * 55)

    success_p = success_l = failed = 0

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--single-process",
                "--no-zygote",
            ]
        )
        context = await browser.new_context(
            viewport=VIEWPORT,
            ignore_https_errors=True,
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )

        # ── Capture phishing screenshots ──────────────────────
        print("\n[1/2] Capturing PHISHING screenshots...")
        for i, row in tqdm(phish_df.iterrows(), total=len(phish_df),
                           bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'):
            fname = f"phish_{i:04d}.png"
            if fname in existing_phish:
                continue
            path = os.path.join(PHISH_DIR, fname)
            page = await context.new_page()
            ok   = await capture_screenshot(page, row['url'], path)
            await page.close()
            if ok and os.path.exists(path) and os.path.getsize(path) > 1000:
                success_p += 1
            else:
                if os.path.exists(path):
                    os.remove(path)
                failed += 1

        # ── Capture legitimate screenshots ────────────────────
        print("\n[2/2] Capturing LEGITIMATE screenshots...")
        for i, row in tqdm(legit_df.iterrows(), total=len(legit_df),
                           bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'):
            fname = f"legit_{i:04d}.png"
            if fname in existing_legit:
                continue
            path = os.path.join(LEGIT_DIR, fname)
            page = await context.new_page()
            ok   = await capture_screenshot(page, row['url'], path)
            await page.close()
            if ok and os.path.exists(path) and os.path.getsize(path) > 1000:
                success_l += 1
            else:
                if os.path.exists(path):
                    os.remove(path)
                failed += 1

        await browser.close()

    # ── Final summary ─────────────────────────────────────────
    total_p = len([f for f in os.listdir(PHISH_DIR) if f.endswith('.png')])
    total_l = len([f for f in os.listdir(LEGIT_DIR) if f.endswith('.png')])

    print("\n" + "=" * 55)
    print("  📊 CAPTURE SUMMARY")
    print("=" * 55)
    print(f"  ✅ New phishing captured  : {success_p}")
    print(f"  ✅ New legitimate captured: {success_l}")
    print(f"  ❌ Failed                 : {failed}")
    print(f"  📸 TOTAL phishing         : {total_p}")
    print(f"  📸 TOTAL legitimate       : {total_l}")
    print(f"  📸 TOTAL dataset          : {total_p + total_l}")
    print("=" * 55)
    print("\n✅ Done! Upload to Google Colab and retrain.")


if __name__ == "__main__":
    asyncio.run(main())

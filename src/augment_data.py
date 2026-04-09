"""
PhishViT — Data Augmentation Script
Author: Jean Chrysostome NDAYISABYE
University of Rwanda, Department of Information Systems

Balances the dataset by augmenting the minority class (legitimate)
to match the phishing class count.

Usage:
    python augment_data.py
"""

import os
import random
from PIL import Image, ImageEnhance, ImageFilter
from tqdm import tqdm

# ── Config ─────────────────────────────────────────────────────
PHISH_DIR  = os.path.expanduser("~/phishvit/data/phishing")
LEGIT_DIR  = os.path.expanduser("~/phishvit/data/legitimate")
SEED       = 42

random.seed(SEED)


def augment_image(img: Image.Image) -> Image.Image:
    """Apply a random visual augmentation to an image."""
    ops = [
        lambda x: ImageEnhance.Brightness(x).enhance(random.uniform(0.80, 1.20)),
        lambda x: ImageEnhance.Contrast(x).enhance(random.uniform(0.80, 1.20)),
        lambda x: ImageEnhance.Sharpness(x).enhance(random.uniform(0.75, 1.25)),
        lambda x: ImageEnhance.Color(x).enhance(random.uniform(0.85, 1.15)),
        lambda x: x.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.0, 0.8))),
        lambda x: x.crop((
            random.randint(0, 15), random.randint(0, 15),
            x.width  - random.randint(0, 15),
            x.height - random.randint(0, 15)
        )).resize(x.size, Image.LANCZOS),
    ]
    # Apply 1 or 2 random operations
    n_ops = random.choice([1, 2])
    selected = random.sample(ops, n_ops)
    for op in selected:
        img = op(img)
    return img


def main():
    # Count existing images
    phish_imgs = [f for f in os.listdir(PHISH_DIR) if f.endswith('.png')]
    legit_imgs = [f for f in os.listdir(LEGIT_DIR) if f.endswith('.png')]

    n_phish = len(phish_imgs)
    n_legit = len(legit_imgs)
    needed  = n_phish - n_legit

    print("=" * 50)
    print("  PhishViT — Data Augmentation")
    print("=" * 50)
    print(f"  Phishing   : {n_phish}")
    print(f"  Legitimate : {n_legit}")
    print(f"  Target     : {n_phish} (match phishing)")
    print(f"  To augment : {max(0, needed)}")
    print("=" * 50)

    if needed <= 0:
        print("✅ Dataset already balanced! No augmentation needed.")
        return

    print(f"\nAugmenting {needed} legitimate images...")
    count = 0
    for i in tqdm(range(needed), bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'):
        src_file = random.choice(legit_imgs)
        src_path = os.path.join(LEGIT_DIR, src_file)
        try:
            img     = Image.open(src_path).convert("RGB")
            aug_img = augment_image(img)
            out_name = f"legit_aug_{i:04d}.png"
            aug_img.save(os.path.join(LEGIT_DIR, out_name))
            count += 1
        except Exception as e:
            print(f"⚠️  Skipped {src_file}: {e}")

    # Final counts
    total_legit = len([f for f in os.listdir(LEGIT_DIR) if f.endswith('.png')])
    total_phish = len([f for f in os.listdir(PHISH_DIR) if f.endswith('.png')])

    print(f"\n✅ Augmentation complete!")
    print(f"   Added            : {count} images")
    print(f"   Total phishing   : {total_phish}")
    print(f"   Total legitimate : {total_legit}")
    print(f"   Total dataset    : {total_phish + total_legit}")

    if total_phish == total_legit:
        print("✅ Dataset is now perfectly balanced!")
    else:
        print(f"⚠️  Small imbalance: {abs(total_phish - total_legit)} difference")


if __name__ == "__main__":
    main()

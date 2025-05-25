sanırım enflasyonu 12 ay öncesiyle karşılaştırmam lazım??

✅ You’re using: TP.FG.J0
This code gives you the Domestic Producer Price Index (D-PPI / Yİ-ÜFE)

The values like 3043.23 are index values (not percentages)

The index has a base year = 2003, which is normalized to 100 in that year

So:
3043.23 means prices are 30.43x higher than in 2003
→ This is not inflation directly, but the raw index.

🔄 So What Should You Do With That?
If you want annual inflation (YoY %), you calculate:

python
Kopyala
Düzenle
YoY_PPI = ((PPI_today / PPI_12_months_ago) - 1) * 100
Example:
Month	PPI Index
Apr 2025	3043.23
Apr 2024	1791.87

python
Kopyala
Düzenle
YoY_PPI = ((3043.23 / 1791.87) - 1) * 100 ≈ 69.86%
➡️ That’s the actual PPI inflation you want to show on your site.

🧠 TL;DR:
TP.FG.J0 is useful, but you need to manually compute the inflation from it.

You can also fetch 13 months of values and calculate YoY inflation yourself.

These index values are not directly interpretable as inflation without that step.

👉 If You Want Consumer Inflation (CPI):
Unfortunately, it looks like consumer inflation (TÜFE) data might only be available as index values too (not percentage change) on EVDS under TP.FG.m() or similar.

So your site will likely need to calculate both CPI and PPI inflation rates from index data. I can give you a Python snippet to do this in 10 lines — just say the word.
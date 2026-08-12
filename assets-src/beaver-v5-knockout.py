"""Knock the flat black disc out of the Battle Beaver badge.

Input:  assets-src/widgets/beaver-v4.png  (keyed + desaturated badge)
Output: assets-src/widgets/beaver-v5.png  (disc field transparent)
        public/images/widgets/beaver-v5.webp

A plain luminance key drops the disc field but also eats the minigun, which is
dark metal. So the key is combined with a local-contrast ("ink") term: the gun,
beaver and lettering carry dense linework and stay opaque, while the flat grunge
field falls away and lets the page background show through the ring.
"""
from PIL import Image
import numpy as np
from scipy import ndimage

src = Image.open('assets-src/widgets/beaver-v4.png').convert('RGBA')
a = np.asarray(src).astype(float)
rgb, al = a[..., :3], a[..., 3] / 255.0
lum = rgb.mean(axis=2)

# local contrast, blurred so single grunge specks in the flat field don't count
g = ndimage.uniform_filter(lum, 7)
sd = np.sqrt(np.clip(ndimage.uniform_filter(lum ** 2, 7) - g ** 2, 0, None))
ink = np.clip(ndimage.gaussian_filter(np.clip((sd - 8) / 22.0, 0, 1), 3) * 1.5, 0, 1)

base = np.clip((lum - 30) / 60.0, 0, 1) ** 0.8
alpha = al * np.clip(base + 0.85 * ink, 0, 1)

out = Image.fromarray(np.dstack([rgb, alpha * 255]).astype(np.uint8), 'RGBA')
out.save('assets-src/widgets/beaver-v5.png')

# the soft alpha channel dominates the file size here, so trade a little alpha
# precision (indistinguishable at the ~190px display height) for ~40% off
w = 440
out.resize((w, round(out.height * w / out.width)), Image.LANCZOS).save(
    'public/images/widgets/beaver-v5.webp', 'WEBP', quality=76, method=6, alpha_quality=70)
print('wrote beaver-v5', out.size)

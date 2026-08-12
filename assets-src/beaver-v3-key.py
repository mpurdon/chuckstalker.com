from PIL import Image
import numpy as np
from scipy import ndimage

SRC = '/Users/mp/.claude/image-cache/c7d7c40e-c614-4c1c-9809-bf99b3431226/1.png'
im = Image.open(SRC).convert('RGB')
a = np.asarray(im).astype(float)
lum = a.mean(axis=2)
h, w = lum.shape

# --- isolate the main emblem, dropping the neighbouring-sticker crop artifacts
mask = lum < 225
mask = ndimage.binary_closing(mask, np.ones((3, 3)))
lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
sizes = ndimage.sum(mask, lab, range(1, n + 1))
main = (lab == (np.argmax(sizes) + 1))
main = ndimage.binary_fill_holes(main)

# --- fit the badge circle: largest inscribed circle of the filled silhouette
dist = ndimage.distance_transform_edt(main)
cy, cx = np.unravel_index(np.argmax(dist), dist.shape)
r = dist[cy, cx]
print('circle center', cx, cy, 'radius', r)

yy, xx = np.mgrid[0:h, 0:w]
rad = np.hypot(xx - cx, yy - cy)

# soft alpha from "distance to white" for the parts sticking out of the circle
soft = np.clip((248.0 - lum) / 45.0, 0, 1)
outside = main & (rad > r)
outside = ndimage.binary_opening(outside, np.ones((3, 3)))   # kill speckle
outside = ndimage.binary_dilation(outside, np.ones((3, 3)), iterations=2)

alpha = np.zeros((h, w))
# inside the badge: fully opaque, with a 1.5px feather at the rim
alpha = np.maximum(alpha, np.clip((r + 0.5 - rad) / 1.5, 0, 1))
alpha = np.maximum(alpha, soft * outside)

rgba = np.dstack([a, alpha * 255]).astype(np.uint8)
out = Image.fromarray(rgba, 'RGBA')

# --- crop to content
bb = ndimage.find_objects(ndimage.binary_fill_holes(alpha > 0.08).astype(int))[0]
y0, y1 = bb[0].start, bb[0].stop
x0, x1 = bb[1].start, bb[1].stop
print('crop', x0, y0, x1, y1)
out = out.crop((x0, y0, x1, y1))
out.save('/private/tmp/claude-501/-Users-mp-Projects-chuckstalker-com/c7d7c40e-c614-4c1c-9809-bf99b3431226/scratchpad/beaver-v3.png')
print('out size', out.size)

# checkerboard preview so transparency is visible
prev = Image.new('RGB', out.size, 'white')
px = np.asarray(prev).copy()
yy2, xx2 = np.mgrid[0:out.size[1], 0:out.size[0]]
chk = ((yy2 // 12 + xx2 // 12) % 2) == 0
px[chk] = (200, 200, 200)
prev = Image.fromarray(px)
prev.paste(out, (0, 0), out)
prev.save('/private/tmp/claude-501/-Users-mp-Projects-chuckstalker-com/c7d7c40e-c614-4c1c-9809-bf99b3431226/scratchpad/beaver-v3-preview.png')

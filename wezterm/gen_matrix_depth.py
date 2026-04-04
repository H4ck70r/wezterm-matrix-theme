#!/usr/bin/env python3
"""Matrix rain with depth layers - blurry background + sharp foreground"""
import random
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 960, 540
FPS = 8
DURATION_SEC = 20
FRAMES = FPS * DURATION_SEC
CELL_W = 11
CELL_H = 14
COLS = W // CELL_W
ROWS = H // CELL_H

CHARS = list(
    "ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿ"
    "ﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜ"
    "012345789:.<>=+*|¦"
)

try:
    font_sm = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 9)
    font_md = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 11)
    font_lg = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 13)
except:
    font_sm = font_md = font_lg = ImageFont.load_default()

class Stream:
    def __init__(self, layer):
        self.col = 0
        self.layer = layer  # 0=far/blurry, 1=mid, 2=near/sharp
        self.reset(True)

    def reset(self, init=False):
        self.y = random.uniform(-ROWS * 3, ROWS) if init else random.uniform(-ROWS * 1.2, -3)
        # 4 speed tiers for all layers: 0.02-0.10 range
        tier = random.choice(['crawl', 'slow', 'medium', 'brisk'])
        if tier == 'crawl':
            self.speed = random.uniform(0.02, 0.035)
        elif tier == 'slow':
            self.speed = random.uniform(0.035, 0.055)
        elif tier == 'medium':
            self.speed = random.uniform(0.055, 0.075)
        else:
            self.speed = random.uniform(0.075, 0.09)
        len_ranges = {0: (4, 18), 1: (6, 28), 2: (8, 35)}
        lo, hi = len_ranges[self.layer]
        self.length = random.randint(lo, hi)
        self.chars = [random.choice(CHARS) for _ in range(self.length)]
        self.flicker = random.uniform(0.12, 0.4)
        self.pause_timer = 0
        self.pause_chance = random.uniform(0.001, 0.006)
        # Track which chars just changed for white flash
        self.just_changed = set()

    def update(self):
        self.just_changed.clear()
        if self.pause_timer > 0:
            self.pause_timer -= 1
            for i in range(self.length):
                if random.random() < self.flicker:
                    self.chars[i] = random.choice(CHARS)
                    self.just_changed.add(i)
            return
        if random.random() < self.pause_chance:
            self.pause_timer = random.randint(3, 10)
            return
        self.y += self.speed
        for i in range(self.length):
            if random.random() < self.flicker:
                self.chars[i] = random.choice(CHARS)
                self.just_changed.add(i)
        if self.y - self.length > ROWS + 5:
            self.reset()

# Create streams in 3 layers - high density
streams_by_layer = {0: [], 1: [], 2: []}
for x in range(COLS):
    # Far layer: dense background wash
    for _ in range(random.randint(1, 3)):
        s = Stream(0); s.col = x
        streams_by_layer[0].append(s)
    # Mid layer: dense
    for _ in range(random.randint(2, 3)):
        s = Stream(1); s.col = x
        streams_by_layer[1].append(s)
    # Near layer: dense
    for _ in range(random.randint(1, 2)):
        s = Stream(2); s.col = x
        streams_by_layer[2].append(s)

# Warm up all layers
for layer_streams in streams_by_layer.values():
    for _ in range(ROWS * 5):
        for s in layer_streams:
            s.update()

fonts = {0: font_sm, 1: font_md, 2: font_lg}
os.makedirs('/tmp/matrix_frames2', exist_ok=True)
print(f"Generating {FRAMES} frames with depth layers...")

for frame in range(FRAMES):
    if frame % 20 == 0:
        print(f"  {frame}/{FRAMES}")

    # Layer 0: far background (will be blurred)
    img_far = Image.new('RGB', (W, H), (0, 0, 0))
    draw_far = ImageDraw.Draw(img_far)

    # Layer 1: mid
    img_mid = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_mid = ImageDraw.Draw(img_mid)

    # Layer 2: near foreground (sharp)
    img_near = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_near = ImageDraw.Draw(img_near)

    layer_imgs = {0: (img_far, draw_far), 1: (img_mid, draw_mid), 2: (img_near, draw_near)}

    for layer in [0, 1, 2]:
        img_l, draw_l = layer_imgs[layer]
        brightness_mult = {0: 0.3, 1: 0.7, 2: 1.0}[layer]
        f = fonts[layer]

        for stream in streams_by_layer[layer]:
            head_y = stream.y
            x = stream.col
            for i in range(stream.length):
                cy = int(head_y - i)
                if 0 <= cy < ROWS:
                    ch = stream.chars[i]
                    px = x * CELL_W
                    py = cy * CELL_H
                    bm = brightness_mult

                    # Characters that just changed: flash bright - always visible regardless of layer
                    if i in stream.just_changed and i > 0:
                        flash_bm = max(0.7, bm)  # minimum brightness for flash
                        g_val = int(255 * flash_bm)
                        color = (int(g_val * 0.7), g_val, int(g_val * 0.6))
                    elif i == 0:
                        # Head: bright green with slight white tint
                        color = (int(60 * bm), int(255 * bm), int(50 * bm))
                    elif i == 1:
                        color = (int(20 * bm), int(240 * bm), int(30 * bm))
                    elif i < 4:
                        color = (0, int(210 * bm), int(20 * bm))
                    else:
                        t = (i - 4) / max(1, stream.length - 4)
                        g = max(4, int(150 * (1.0 - t) ** 1.8 * bm))
                        color = (0, g, max(0, g // 12))

                    if layer == 0:
                        draw_l.text((px, py), ch, fill=color, font=f)
                    else:
                        color_a = color + (255,)
                        draw_l.text((px, py), ch, fill=color_a, font=f)

            stream.update()

    # Blur the far layer
    img_far = img_far.filter(ImageFilter.GaussianBlur(radius=2.5))

    # Slight blur on mid layer
    img_mid_rgb = Image.new('RGB', (W, H), (0, 0, 0))
    img_mid_rgb.paste(img_mid, mask=img_mid.split()[3])
    img_mid_rgb = img_mid_rgb.filter(ImageFilter.GaussianBlur(radius=0.8))

    # Composite: far + mid + near
    final = img_far.copy()
    final = Image.blend(final, img_mid_rgb, 0.7)
    # Paste near layer on top (sharp)
    final.paste(img_near, mask=img_near.split()[3])

    final.save(f'/tmp/matrix_frames2/frame_{frame:04d}.png')

print("Creating optimized GIF...")
output = os.path.expanduser('~/.config/wezterm/matrix-rain-generated.gif')
os.system(
    f'ffmpeg -y -framerate {FPS} -i /tmp/matrix_frames2/frame_%04d.png '
    f'-vf "fps={FPS},palettegen=max_colors=96:stats_mode=diff" '
    f'/tmp/matrix_palette3.png 2>/dev/null && '
    f'ffmpeg -y -framerate {FPS} -i /tmp/matrix_frames2/frame_%04d.png '
    f'-i /tmp/matrix_palette3.png '
    f'-lavfi "fps={FPS} [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=2" '
    f'-loop 0 {output} 2>/dev/null'
)

import shutil
shutil.rmtree('/tmp/matrix_frames2')
for f in ['/tmp/matrix_palette3.png']:
    if os.path.exists(f): os.remove(f)

size_mb = os.path.getsize(output) / (1024*1024)
print(f"Done! {output} ({size_mb:.1f}MB, {FRAMES} frames)")

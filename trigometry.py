import math


radius = 10
steps = 36
step = 360 / steps

data = []

for i in range(steps):
    angle = i * step
    print(angle, math.tan(angle))
    coords = [radius * math.sin(math.radians(angle)), radius * math.cos(math.radians(angle))]
    for i, c in enumerate(coords):
        if c < 0:
            coords[i] = str(c)[:5]
        else:
            coords[i] = str(c)[:4]
    data.append(coords)

for c in data:
    print(f'{c[0]}, {c[1]}')
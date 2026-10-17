import math
import xml.etree.ElementTree as ET

NS = {"g": "http://www.topografix.com/GPX/1/1"}
R = 6371008.8


def load(path):
    root = ET.parse(path).getroot()
    pts = [
        (float(p.get("lat")), float(p.get("lon")), float(p.find("g:ele", NS).text))
        for p in root.iterfind(".//g:trkpt", NS)
    ]
    wpts = [
        {
            "lat": float(w.get("lat")),
            "lon": float(w.get("lon")),
            "name": (w.findtext("g:name", "", NS) or "").strip(),
            "cmt": (w.findtext("g:cmt", "", NS) or "").strip(),
        }
        for w in root.iterfind("g:wpt", NS)
    ]
    return pts, wpts


def hav(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def cumdist(pts):
    out = [0.0]
    for a, b in zip(pts, pts[1:]):
        out.append(out[-1] + hav(a, b))
    return out


def gain(pts, thresh=3.0):
    up = 0.0
    ref = pts[0][2]
    for p in pts[1:]:
        d = p[2] - ref
        if d > thresh:
            up += d
            ref = p[2]
        elif d < -thresh:
            ref = p[2]
    return up


def nearest(pts, q):
    return min(((hav(p, q), i) for i, p in enumerate(pts)), key=lambda t: t[0])


M2MI = 1 / 1609.344
M2FT = 3.28084

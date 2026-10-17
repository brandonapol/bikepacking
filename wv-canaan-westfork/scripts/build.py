import sys
from xml.sax.saxutils import escape

sys.path.insert(0, sys.argv[1])
from gpxlib import load, cumdist, gain, nearest, hav, M2MI, M2FT

out_dir = sys.argv[2]
C, _ = load("source/canaan-valley-forks-of-cheat.gpx")
W, _ = load("source/west-fork-weekender.gpx")

_, j = nearest(C, W[0])
canaan_from_alpena = C[j:] + C[1 : j + 1]
SPLIT_MI = 6.0
dc = cumdist(C)
k_camp = next(i for i, x in enumerate(dc) if x * M2MI >= SPLIT_MI)
day_breaks = [0, len(C) - j - 1 + k_camp, len(canaan_from_alpena)]
route = canaan_from_alpena + W[1:]
day_breaks.append(len(route) - 1)

dist = cumdist(route)
days = [
    ("Day 1 (Fri): Alpena to Canaan Loop Rd camp via Bickle Knob, Shavers Fork, Parsons, Blackwater Canyon, Davis", 0),
    ("Day 2 (Sat): Canaan Loop Rd camp to Alpena via Canaan Valley, Gladwin", 1),
    ("Day 3 (Sun): West Fork loop via Glady, West Fork Rail Trail, Burner, Little River, Middle Mountain", 2),
]

GAIN_THRESH_M = 6.5


def day_slice(k):
    return route[day_breaks[k] : day_breaks[k + 1] + 1]


def loss(pts):
    return gain([(a, b, -e) for a, b, e in pts], GAIN_THRESH_M)


WPTS = [
    ("Alpena Parking (start/finish)", 38.90755, -79.65407, "Parking Area",
     "Route junction on US-33 at Alpena where the Canaan and West Fork loops meet. Confirm exact lot on arrival. Restock here after Day 2.",
     f"Trip mi 0.0 (Day 1 start), {dist[day_breaks[2]] * M2MI:.1f} (end Day 2 / start Day 3), {dist[-1] * M2MI:.1f} (finish)"),
    ("Bear Heaven Campground", 38.931552, -79.680563, "Campground",
     "USFS, FR 91 (Stuart Memorial Dr). First come first served, ~$5, vault toilet, NO potable water. Open mid-Apr to Nov. Thu car camp."),
    ("Gladwin Dispersed Camping", 39.0072, -79.5491, "Campground",
     "Free MNF dispersed, Glady Fork / Dry Fork confluence, Gladwin Rd (CR 12). No facilities, pack it out. Filter water."),
    ("Lower Glady Dispersed Camping (FR 162)", 38.978178, -79.590459, "Campground",
     "MNF designated dispersed sites on Glady Fork near Milus TH. Coordinates differ by source (DispersedApp 38.978,-79.590; Campendium 38.964,-79.607); verify on MNF map. Filter/boil water (giardia reported)."),
    ("Little River Dispersed Camping (FR 17)", 38.632426526265334, -79.76183011846058, "Campground",
     "Several miles of dispersed sites along Little River / FR 17. No facilities or potable water."),
    ("Little River Primitive Campground", 38.65764175419717, -79.72159489501011, "Campground",
     "Free, first come first served."),
    ("West Fork Dispersed Camping (FR 44)", 38.5902, -79.8226, "Campground",
     "FR 44 dispersed sites north of Durbin along West Fork Greenbrier / Rail Trail. OFF ROUTE: south of Burner turn. Coordinates user-submitted; verify."),
    ("Middle Mountain Cabins Hand Pump (WATER)", 38.69151398822395, -79.73349320824225, "Drinking Water",
     "Only potable water on the West Fork loop. Cabins are USFS rentals."),
    ("Food: Parsons", 39.0938, -79.6737, "Restaurant",
     "Groceries and restaurants in Parsons. Last resupply before Blackwater Canyon climb."),
    ("Food: Thomas", 39.1495, -79.4970, "Restaurant",
     "Cafes/restaurants in Thomas."),
    ("Food: Davis", 39.1288399, -79.46318, "Restaurant",
     "Davis: restaurants, breweries, Blackwater Bikes. Eat dinner and fill all water here before riding out to the Canaan Loop Rd camp."),
    ("Blackwater Falls SP Campground (backup)", 39.11613607995228, -79.48913891665221, "Campground",
     "Backup only: state park campground, around $50/night and nearly booked. Dispersed camping NOT allowed in the state park or on private land around Parsons-Thomas-Davis."),
    ("Fri Camp: Canaan Loop Rd Dispersed", route[day_breaks[1]][0], route[day_breaks[1]][1], "Campground",
     "Free MNF dispersed camping 100+ ft off Canaan Loop Rd (FR 13). Target point only: confirm in onX that you are past the Blackwater Falls SP boundary, then pick any flat spot. No water, toilets or tables."),
    ("Bickle Knob Tower (spur)", 38.93410495546047, -79.73149166037656, "Scenic Area",
     "Short out-and-back spur to the fire tower."),
    ("Hike-a-bike to Little River Rd", 38.61708314623242, -79.80753902108337, "Danger Area",
     "Short 100 yd path from the rail trail over to the road at Burner."),
]


def milepost(lat, lon):
    d, i = nearest(route, (lat, lon, 0))
    k = next(n for n in range(3) if day_breaks[n] <= i <= day_breaks[n + 1])
    return d, dist[i] * M2MI, (dist[i] - dist[day_breaks[k]]) * M2MI, k + 1


def trkpts(pts, indent):
    return "\n".join(
        f'{indent}<trkpt lat="{la:.6f}" lon="{lo:.6f}"><ele>{e:.1f}</ele></trkpt>' for la, lo, e in pts
    )


def wpt_xml(name, lat, lon, sym, desc, fixed_note=None):
    off, total, day_mi, day = milepost(lat, lon)
    note = fixed_note or f"Day {day} mi {day_mi:.1f} / trip mi {total:.1f}"
    if off > 150:
        note += f" ({off * M2MI:.1f} mi off route)"
    full = f"{note}. {desc}"
    return (
        f'  <wpt lat="{lat:.6f}" lon="{lon:.6f}">\n'
        f"    <name>{escape(name)}</name>\n"
        f"    <cmt>{escape(full)}</cmt>\n"
        f"    <desc>{escape(full)}</desc>\n"
        f"    <sym>{sym}</sym>\n"
        f"  </wpt>"
    ), (name, day, day_mi, total, off)


HEADER = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<gpx version="1.1" creator="quark-project WV bikepacking planner" '
    'xmlns="http://www.topografix.com/GPX/1/1" '
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
    'xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\n'
)

wxml, wrows = zip(*(wpt_xml(*w) for w in WPTS))
title = "WV Canaan + West Fork 3-Day Loop from Alpena"

single = (
    HEADER
    + f"  <metadata><name>{title}</name></metadata>\n"
    + "\n".join(wxml)
    + f"\n  <trk>\n    <name>{title}</name>\n    <trkseg>\n"
    + trkpts(route, "      ")
    + "\n    </trkseg>\n  </trk>\n</gpx>\n"
)
by_day = (
    HEADER
    + f"  <metadata><name>{title} (by day)</name></metadata>\n"
    + "\n".join(wxml)
    + "\n"
    + "\n".join(
        f"  <trk>\n    <name>{escape(n)}</name>\n    <trkseg>\n" + trkpts(day_slice(k), "      ") + "\n    </trkseg>\n  </trk>"
        for n, k in days
    )
    + "\n</gpx>\n"
)
open(f"{out_dir}/wv-canaan-westfork-loop.gpx", "w").write(single)
open(f"{out_dir}/wv-canaan-westfork-loop-by-day.gpx", "w").write(by_day)

print(f"TOTAL {dist[-1] * M2MI:.1f} mi, gain {gain(route, GAIN_THRESH_M) * M2FT:.0f} ft, points {len(route)}")
for n, k in days:
    p = day_slice(k)
    print(f"{n}: {(dist[day_breaks[k + 1]] - dist[day_breaks[k]]) * M2MI:.1f} mi, +{gain(p, GAIN_THRESH_M) * M2FT:.0f} ft / -{loss(p) * M2FT:.0f} ft, high {max(e for *_, e in p) * M2FT:.0f} ft, low {min(e for *_, e in p) * M2FT:.0f} ft")
for name, day, dm, tm, off in wrows:
    print(f"  {name:42s} day {day} mi {dm:5.1f}  trip mi {tm:6.1f}  off {off * M2MI:.2f} mi")
print("gap junction m:", round(hav(C[j], W[0])))

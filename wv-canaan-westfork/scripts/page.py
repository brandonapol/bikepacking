import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gpxlib import load, cumdist, gain, M2MI, M2FT

ROOT = Path(__file__).resolve().parent.parent
GAIN_THRESH_M = 6.5
SAMPLE_MI = 0.05

C, _ = load(ROOT / "source/canaan-valley-forks-of-cheat.gpx")
W, _ = load(ROOT / "source/west-fork-weekender.gpx")


def nearest_idx(pts, q):
    return min(range(len(pts)), key=lambda i: (pts[i][0] - q[0]) ** 2 + ((pts[i][1] - q[1]) * math.cos(math.radians(q[0]))) ** 2)


j = nearest_idx(C, W[0])
SPLIT_MI = 6.0
dc = cumdist(C)
k = next(i for i, x in enumerate(dc) if x * M2MI >= SPLIT_MI)
FRI_DAVIS = round(cumdist(C[j:])[-1] * M2MI, 1)
day_pts = [C[j:] + C[1 : k + 1], C[k : j + 1], W]

DAY_META = [
    {"id": "fri", "label": "Fri", "title": "Alpena to Canaan Loop Rd", "via": "Bickle Knob, Shavers Fork, Parsons, Blackwater Canyon, Davis"},
    {"id": "sat", "label": "Sat", "title": "Canaan Loop Rd to Alpena", "via": "Canaan Mountain, Canaan Valley, Gladwin"},
    {"id": "sun", "label": "Sun", "title": "West Fork loop", "via": "Glady, West Fork Rail Trail, Little River, Middle Mountain"},
]


def sample(pts):
    d = cumdist(pts)
    out, nxt, i = [], 0.0, 0
    total = d[-1] * M2MI
    while nxt <= total:
        while i < len(d) - 1 and d[i + 1] * M2MI < nxt:
            i += 1
        p = pts[i]
        out.append([round(p[0], 5), round(p[1], 5), round(p[2] * M2FT), round(nxt, 2)])
        nxt = round(nxt + SAMPLE_MI, 2)
    last = pts[-1]
    out.append([round(last[0], 5), round(last[1], 5), round(last[2] * M2FT), round(total, 2)])
    return out, d


def simplify(pts, d, tol_m=6.0):
    k = math.cos(math.radians(pts[0][0]))
    xy = [(p[1] * 111320 * k, p[0] * 110570) for p in pts]
    keep = {0, len(pts) - 1}
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        (ax, ay), (bx, by) = xy[a], xy[b]
        dx, dy = bx - ax, by - ay
        norm = math.hypot(dx, dy) or 1e-9
        far, idx = 0.0, None
        for i in range(a + 1, b):
            dist = abs(dy * (xy[i][0] - ax) - dx * (xy[i][1] - ay)) / norm
            if dist > far:
                far, idx = dist, i
        if idx is not None and far > tol_m:
            keep.add(idx)
            stack += [(a, idx), (idx, b)]
    return [[round(pts[i][0], 5), round(pts[i][1], 5), round(d[i] * M2MI, 2)] for i in sorted(keep)]


def slice_pts(pts, d, a, b):
    return [p for p, x in zip(pts, d) if a <= x * M2MI <= b]


def stats(pts, d, a, b):
    s = slice_pts(pts, d, a, b)
    if len(s) < 2:
        return 0, 0
    return round(gain(s, GAIN_THRESH_M) * M2FT), round(gain([(x, y, -e) for x, y, e in s], GAIN_THRESH_M) * M2FT)


def at(pts, d, mi):
    i = min(range(len(d)), key=lambda k: abs(d[k] * M2MI - mi))
    return pts[i]


STEPS = {
    "fri": [
        (0.0, 1.8, "Climb US-33 to Alpena Gap", "US-33", "paved",
         "Leave the Alpena lot and climb US-33 west toward the top of Shavers Mountain. Traffic moves fast, so stay right."),
        (1.8, 7.8, "Right onto FR 91, Stuart Memorial Dr", "FR 91", "gravel",
         "Turn right (north) at Alpena Gap onto Stuart Memorial Drive. Steady gravel climb. Bear Heaven Campground is on the left about 2.5 mi up."),
        (7.8, 8.6, "Out-and-back to Bickle Knob tower", "FR 91A", "gravel",
         "Short spur up FR 91A to the fire tower, 360 degree views over Shavers Fork and Cheat Mountain. Return the same way to FR 91."),
        (8.6, 12.5, "Descend to Stuart Recreation Area", "FR 91", "gravel",
         "Long gravel descent off the knob to the Shavers Fork valley near Stuart Recreation Area and Bowden."),
        (12.5, 33.4, "Follow Shavers Fork north to Parsons", "Shavers Fork valley", "gravel",
         "About 20 mi of river-grade riding downstream along the Shavers Fork of the Cheat. Water is easy to find (filter it). Mixed ownership near Parsons, so no dispersed camping there."),
        (33.4, 33.4, "Parsons: resupply", "Parsons", "town",
         "Last full grocery on the route. Stock up for the canyon climb and for Saturday."),
        (33.4, 36.8, "Parsons to Hendricks", "Black Fork valley", "paved",
         "Easy, flat miles along the Black Fork to Hendricks, where the rail trail starts."),
        (36.8, 47.3, "Blackwater Canyon Rail Trail up to Thomas", "Blackwater Canyon Rail Trail", "rail trail",
         "Billed as the steepest rail trail in the US. A steady 10 mi grind up the canyon to Thomas. Rough and rocky in places."),
        (47.3, 47.5, "Thomas", "Thomas", "town",
         "Food, coffee and beer in a small downtown. A short street section here doubles back on itself."),
        (47.5, 51.0, "WV-32 to Davis", "WV-32", "paved",
         "Busy but unavoidable highway stretch into Davis. Ride single file. Eat dinner here and fill every bottle: there is no water at camp."),
        (FRI_DAVIS, FRI_DAVIS + 1.8, "Davis to Blackwater Falls State Park", "Blackwater Falls SP roads", "paved",
         "Roll out of Davis through the state park. No camping until you are past the park boundary."),
        (FRI_DAVIS + 1.8, FRI_DAVIS + SPLIT_MI, "Onto Canaan Loop Rd to camp", "Canaan Loop Rd (FR 13)", "rough 4WD",
         "Past Lindy Point and out of the state park onto Monongahela NF land. Check the public-land layer in onX, then pick a flat spot 100+ ft off the road. Free. No toilets, tables or water. Aim to arrive with daylight left."),
    ],
    "sat": [
        (0.0, 19.5 - SPLIT_MI, "Break camp and finish Canaan Loop Road", "Canaan Loop Rd (FR 13)", "rough 4WD",
         "The rest of the loop road: rugged, often muddy forest road and jeep track around Canaan Mountain. Wide tires help, and the Big Honzo is right at home. Climbs to the day's high point near 3,800 ft before reaching WV-32 at Canaan Heights."),
        (19.5 - SPLIT_MI, 29.0 - SPLIT_MI, "Down into Canaan Valley", "Canaan Valley roads", "mixed",
         "Drop to the valley floor near 3,200 ft and cruise south through Canaan Valley, passing near Canaan Valley State Park and the resort area."),
        (29.0 - SPLIT_MI, 37.5 - SPLIT_MI, "Descend toward Dry Fork and Gladwin", "Dry Fork valley", "mixed",
         "Long descent off the south end of the valley down to the Dry Fork of the Cheat, ending at the Gladwin dispersed camping area."),
        (37.5 - SPLIT_MI, 44.0 - SPLIT_MI, "Climb out of Gladwin", "Gladwin climb", "gravel",
         "The big climb of the day. A 2025 trip report took Sully Road down to Lower Glady dispersed camping from this climb as a bail-out or overnight option."),
        (44.0 - SPLIT_MI, 999, "Roll and descend back to Alpena", "To Alpena", "mixed",
         "Rolling ridge, then a fast drop back to the car. The final mile is the same road you finish on Sunday."),
    ],
    "sun": [
        (0.0, 9.4, "Glady Fork Rd south to Glady", "Glady Fork Rd", "paved",
         "About 9 mi of quiet pavement, rolling along Glady Fork into the hamlet of Glady."),
        (9.4, 9.5, "Glady", "Glady", "town",
         "Glady Presbyterian Church, built 1905 and on the National Register. No services."),
        (9.5, 24.7, "West Fork Rail Trail south", "West Fork Rail Trail", "rail trail",
         "Remote, gentle rail grade along the West Fork of the Greenbrier. Side trip to the old Wildell site around mile 16.4 for photos."),
        (24.7, 24.7, "Hike-a-bike at Burner", "Burner", "trail",
         "Leave the rail trail a few miles before Durbin. A 100 yd path through the woods takes you from the trail over to Little River Road. FR 44 dispersed camping is 2 mi south of here, off route."),
        (24.7, 31.3, "Up Little River", "Little River Rd (FR 17)", "gravel",
         "Gentle climb up the Little River valley. Miles of dispersed sites start around mile 27.7. Little River Primitive Campground at 31.3."),
        (31.3, 35.5, "Climb to Middle Mountain", "Middle Mountain", "gravel",
         "The steepest climb of the day. Fill every bottle at the Middle Mountain Cabins hand pump at mile 34.5. It is the only potable water on this loop."),
        (35.5, 45.6, "Middle Mountain ridge north", "Middle Mountain ridge", "gravel",
         "High, rolling ridge riding past the Laurel Fork area."),
        (45.6, 48.0, "Fast descent to Beaver Dam Run", "Beaver Dam Run", "gravel",
         "Quick drop. Good photo spot near mile 47.8. Watch your speed on loose gravel."),
        (48.0, 52.8, "Climb back toward Alpena", "Final climb", "gravel",
         "Last real climb of the trip."),
        (52.8, 55.7, "Descend to the car at Alpena", "To Alpena", "mixed",
         "Same road as Saturday's finish. Done."),
    ],
}

STOPS = [
    ("fri", 0.0, "park", "Alpena parking", 0, "Start and finish. Confirm the exact lot on arrival.", []),
    ("fri", 4.3, "camp", "Bear Heaven Campground", 0.04, "USFS, first come first served, about $5. Vault toilet, no potable water. Open mid-Apr to Nov. Thursday car camp.", []),
    ("fri", 8.2, "sight", "Bickle Knob tower", 0.03, "Fire tower with 360 degree views.", []),
    ("fri", 12.5, "camp", "Stuart Recreation Area", 0.23, "USFS campground and day use on Shavers Fork.", []),
    ("fri", 33.4, "food", "Parsons", 0, "Groceries and diner food. Last big resupply.", [
        ("Shop 'n Save", "302 D and W Ln. Groceries, listed 8a to 10p daily"),
        ("Dollar General", "515 1st St. Snacks and basics, listed 8a to 11p"),
        ("Trisha's Family Restaurant", "166 Main St. Diner"),
        ("CJ's Pizzeria", "210 Pennsylvania Ave"),
        ("Brenda's Backwoods Grill", "Local favorite, family atmosphere"),
        ("McDonald's / Subway", "1st St"),
    ]),
    ("fri", 47.5, "food", "Thomas", 0.05, "Small downtown with coffee, cafe food and a brewery.", [
        ("Purple Fiddle", "96 East Ave. Deli food, hummus and falafel, live music most nights, hostel upstairs"),
        ("TipTop", "Coffee and baked goods by morning, burgers and drinks at night"),
        ("Mountain State Brewing", "Pub with wood-fired flatbreads"),
        ("Happy & More Bakery and Cafe", "Bakery"),
    ]),
    ("fri", FRI_DAVIS, "food", "Davis", 0, "Dinner and a full water refill before riding out to camp.", [
        ("Sirianni's Cafe", "474 William Ave. Pizza and Italian, cash only per a 2020 review, expect waits"),
        ("Blackwater Brewing Co.", "Brewery"),
        ("Stumptown Ales", "Brewery"),
        ("Sawmill Restaurant", "Diner"),
        ("Hellbender Burritos", "New owners, reopening in 2026. Not confirmed open"),
        ("Blackwater Bikes", "Bike shop"),
    ]),
    ("fri", FRI_DAVIS + 1.8, "camp", "Blackwater Falls SP Campground (backup)", 0.27, "Backup only: around $50 a night and nearly booked.", []),
    ("fri", FRI_DAVIS + SPLIT_MI, "camp", "Friday camp: Canaan Loop Rd dispersed", 0, "Free MNF dispersed camping 100+ ft off FR 13. Confirm you are past the state park boundary in onX. At least seven established sites along the road, the best ones with fire rings are farther east. No water.", []),
    ("sat", 27.9 - SPLIT_MI, "sight", "Canaan Valley State Park", 0.9, "Route passes about 1 mi away. Food options here were not researched.", []),
    ("sat", 37.5 - SPLIT_MI, "camp", "Gladwin dispersed camping", 0.01, "Free MNF site where Glady Fork meets Dry Fork. No facilities, pack it out.", []),
    ("sat", 40.8 - SPLIT_MI, "camp", "Lower Glady dispersed (FR 162)", 1.15, "Off route via Sully Rd. Vault toilets. Filter or boil water, giardia reported. Location differs between sources.", []),
    ("sat", 999, "park", "Back at the car", 0, "Restock food and water for Sunday. Bear Heaven is a 4 mi drive up FR 91 for Saturday night.", []),
    ("sun", 9.5, "sight", "Glady Presbyterian Church", 0.02, "Built 1905.", []),
    ("sun", 24.7, "camp", "West Fork dispersed (FR 44)", 2.0, "Off route, 2 mi south of the Burner turn. Durbin restaurants (Big Al's, Station 2) are another 2 mi beyond.", []),
    ("sun", 27.7, "camp", "Little River dispersed (FR 17)", 0.04, "Several miles of sites. No facilities or potable water.", []),
    ("sun", 31.3, "camp", "Little River Primitive Campground", 0.01, "Free, first come first served.", []),
    ("sun", 34.5, "water", "Middle Mountain hand pump", 0.08, "Only potable water on the West Fork loop. Fill everything.", []),
]

TOWNS = [
    ("Alpena", 38.9075, -79.6541),
    ("Parsons", 39.0968, -79.6809),
    ("Hendricks", 39.0743, -79.6326),
    ("Thomas", 39.1495, -79.4970),
    ("Davis", 39.1287, -79.4654),
    ("Canaan Valley", 39.0450, -79.4400),
    ("Gladwin", 39.0072, -79.5491),
    ("Glady", 38.7973, -79.7192),
    ("Burner", 38.6171, -79.8080),
    ("Bickle Knob", 38.9341, -79.7315),
]


def build():
    days = []
    steps = []
    stops = []
    for meta, pts in zip(DAY_META, day_pts):
        smp, d = sample(pts)
        g, l = stats(pts, d, 0, 999)
        miles = round(d[-1] * M2MI, 1)
        days.append({**meta, "miles": miles, "gain": g, "loss": l, "pts": smp, "line": simplify(pts, d)})
        for a, b, title, road, surface, body in STEPS[meta["id"]]:
            a, b = round(min(a, miles), 2), round(min(b, miles), 2)
            sg, sl = stats(pts, d, a, b)
            p = at(pts, d, a)
            steps.append({"day": meta["id"], "a": a, "b": b, "title": title, "road": road, "surface": surface,
                          "body": body, "gain": sg, "loss": sl, "lat": round(p[0], 5), "lon": round(p[1], 5)})
        for day, mi, kind, name, off, note, options in STOPS:
            if day != meta["id"]:
                continue
            mi = round(min(mi, miles), 2)
            p = at(pts, d, mi)
            stops.append({"day": day, "mi": mi, "kind": kind, "name": name, "off": off, "note": note,
                          "options": [{"name": n, "detail": x} for n, x in options],
                          "lat": round(p[0], 5), "lon": round(p[1], 5)})
    return {"days": days, "steps": steps, "stops": stops,
            "towns": [{"name": n, "lat": la, "lon": lo} for n, la, lo in TOWNS]}


def main():
    template = (ROOT / "scripts/template.html").read_text()
    leaflet_css = (ROOT / "scripts/vendor/leaflet-1.9.4.css").read_text()
    body = template.replace("__LEAFLET_CSS__", leaflet_css).replace("__DATA__", json.dumps(build(), separators=(",", ":")))
    out_fragment = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if out_fragment:
        out_fragment.write_text(body)
    (ROOT.parent / "index.html").write_text(
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        "</head>\n<body>\n" + body + "\n</body>\n</html>\n"
    )


main()

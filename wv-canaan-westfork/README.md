# WV bikepacking: Canaan Valley + West Fork combined loop

Researched 2026-10-17 for Brandon's 4-day trip (Thu drive from Dayton, Fri–Sun riding, Kona Big Honzo).
The goal was to merge two bikepacking.com routes into one loop that starts and ends at Alpena (US-33).

## Files

| File | What it is |
| --- | --- |
| `wv-canaan-westfork-loop.gpx` | One continuous track plus 14 waypoints. Use this for **Ride with GPS** (imports as one route). |
| `wv-canaan-westfork-loop-by-day.gpx` | The same line split into 3 tracks (Fri/Sat/Sun) plus the same waypoints. Use this for **onX Backcountry**: each day shows up as its own line. |
| `source/` | The original GPX files: [Canaan Valley & Forks of Cheat](https://bikepacking.com/wp-content/uploads/2021/02/Canaan-Valley-and-the-Forks-of-Cheat-bikepacking-route.gpx) ([RWGPS 35116010](https://ridewithgps.com/routes/35116010)) and [West Fork Weekender](https://bikepacking.com/wp-content/uploads/2020/12/West-Fork-Weekender-Bikepacking-Route.gpx) ([RWGPS 34771169](https://ridewithgps.com/routes/34771169)). |
| `scripts/build.py` | Rebuilds both GPX outputs: `python3 -I scripts/build.py scripts .` from this folder. |
| `../index.html`, `scripts/page.py`, `scripts/template.html` | The shareable trip page (Leaflet map) at the repo root for GitHub Pages. Rebuild with `python3 -I scripts/page.py` from this folder. |

Both outputs are GPX 1.1 and pass an `xmllint` well-formedness check. Every waypoint's description starts with its day milepost.

## How the two routes connect

- **Canaan** is a 101.6 mi loop that starts and ends in Davis (Blackwater Bikes). **West Fork** is a 55.8 mi loop that starts and ends at Alpena (38.90755, -79.65407).
- The West Fork start is 18 m from the Canaan track at **Canaan mi 50.6**. That point is the junction and the parking spot.
- **Shared track.** Both routes come into Alpena on the same roads from the east:
  - Exact overlap for 1.1 mi: WF mi 52.84–53.04 (0.2 mi) and WF mi 54.81–55.75 (0.94 mi). These line up with Canaan mi 47.3–47.5 and 49.7–50.6.
  - Between those two pieces the routes run on parallel lines 80–350 m apart for about 1.8 mi.
  - You ride all of this twice, both times in the same direction: on the Sat finish and again on the Sun finish. Nothing else is shared between the routes.
- **Repeated sections inside Canaan.** The Bickle Knob tower spur is a short out-and-back (~0.2 mi each way, Day 1 mi ~7.8–8.4). There is also a ~0.2 mi doubled street section in Thomas. West Fork has no repeated sections.
- **Order.** The combined route is Canaan from mi 50.6 → Davis → 6 mi onto Canaan Loop Rd (Day 1), then on around to mi 50.6 (Day 2), then the full West Fork loop (Day 3). The Canaan GPX already runs in the direction of the plan (Bickle Knob/Shavers Fork first), so neither route is reversed.

## Day splits

The gain numbers below are recomputed from the GPX elevations, counting only climbs larger than 6.5 m. That setting reproduces the published totals within about 1%: 8,145 ft computed vs 8,063 published for Canaan, and 3,898 vs 3,907 for West Fork.

| Day | Route | Miles | Gain | Loss | High / low |
| --- | --- | ---: | ---: | ---: | --- |
| Thu | Dayton → Point Pleasant (Mothman) → Bear Heaven, drive and car camp | – | – | – | – |
| Fri | Alpena → Bear Heaven → Bickle Knob → Stuart → Shavers Fork → Parsons → Hendricks → Blackwater Canyon RT → Thomas → Davis → Canaan Loop Rd camp | **57.0** | **+4,596 ft** | −4,123 | 4,007 / 1,638 ft |
| Sat | Canaan Loop Rd camp → Canaan Valley → Laneville/Dry Fork → Gladwin → climb to Alpena | **44.6** | **+3,587 ft** | −4,079 | 3,808 / 1,955 ft |
| Sun | Alpena → Glady → West Fork RT → Burner → Little River → Middle Mountain → Alpena | **55.7** | **+3,898 ft** | −3,893 | 3,892 / 2,630 ft |
| **Total** | | **157.4** | **+12,061 ft** | | |

## Waypoints and mileposts

| Waypoint | Day / day mi | Trip mi | Off route | Notes |
| --- | --- | ---: | ---: | --- |
| Alpena Parking (start/finish) | Fri 0 / Sat 44.6 / Sun 0 & 55.7 | 0 / 101.6 / 157.4 | – | US-33 junction where the two loops meet. Confirm the exact lot on arrival. |
| Bear Heaven Campground | Fri 4.3 | 4.3 | 0.04 | USFS, FR 91. Coordinates from the [USFS page](https://www.fs.usda.gov/r09/monongahela/recreation/bear-heaven-campground). FCFS, ~$5, vault toilet, **no potable water**, open mid-Apr–Nov. |
| Bickle Knob Tower (spur) | Fri 8.2 | 8.2 | 0.03 | |
| Food: Parsons | Fri 33.4 | 33.4 | 0 | |
| Food: Thomas | Fri 47.5 | 47.5 | 0.05 | |
| Food: Davis | Fri 51.0 | 51.0 | 0 | Dinner and a full water refill before camp. Blackwater Bikes is here. |
| Blackwater Falls SP Campground (backup) | Fri 52.8 | 52.8 | 0.27 | Around $50/night and only one spot left when checked. Backup only. |
| **Fri camp: Canaan Loop Rd dispersed** | Fri 57.0 | 57.0 | 0 | Free MNF dispersed camping 100+ ft off FR 13. The point is a target: confirm in onX you are past the state park boundary. No water ([Campendium](https://www.campendium.com/canaan-loop-road-dispersed-camping)). |
| Gladwin Dispersed Camping | Sat 31.4 | 88.5 | 0.01 | Matches the "Dispersed Campground" waypoint in the Canaan GPX. Free MNF site at the Glady Fork/Dry Fork confluence, no facilities ([Campendium](https://www.campendium.com/gladwin-dispersed-camping-area)). |
| Lower Glady Dispersed (FR 162) | Sat ~34.8 | 91.8 | **1.15** | Off-route spur. Sources disagree on location: [DispersedApp](https://dispersedapp.com/camp/colorado/16109-lower-glady-dispersed-camp-site/) gives 38.978,-79.590 (used here), [Campendium](https://maps.campendium.com/us/wv/camping-rv/lower-glady-dispersed-camping-area) gives 38.964,-79.607 (1.8 mi off route). Check the MNF map. Vault toilets. Giardia reported in the water. |
| Hike-a-bike to Little River Rd | Sun 24.7 | 126.4 | 0.02 | 100 yd path from the rail trail to the road at Burner. |
| West Fork Dispersed (FR 44) | Sun ~24.7 | 126.4 | **2.0** | Off route. FR 44 north of Durbin, 2 mi south of the Burner turn ([Campendium](https://www.campendium.com/forest-road-44-dispersed-camping-loop), user-submitted coordinates). |
| Little River Dispersed (FR 17) | Sun 27.7 | 129.3 | 0.04 | Miles of dispersed sites, no facilities or potable water. |
| Little River Primitive Campground | Sun 31.3 | 132.9 | 0.01 | Free, FCFS. |
| **Middle Mountain Cabins hand pump** | Sun 34.5 | 136.1 | 0.08 | **Only potable water on the West Fork loop.** |

## Food on route

Researched 2026-10-17 from web search summaries. Most sources are older, so check current hours. The GPX has one waypoint per town, not one per business.

- **Parsons (Fri mi 33.4).** Groceries: Shop 'n Save (302 D and W Ln, listed 8a–10p), Dollar General (515 1st St). Food: Trisha's Family Restaurant (166 Main St), CJ's Pizzeria (210 Pennsylvania Ave), Brenda's Backwoods Grill, McDonald's, Subway ([Tucker County FAQ](https://tuckercounty.wv.gov/Pages/county-faq.aspx), [Parsons Advocate](https://parsonsadvocate.com/news/pa-top-stories/shop-n-save-hosts-grand-opening-event/), [Mapdoor](https://mapdoor.com/us/wv/parsons)).
- **Thomas (Fri mi 47.5).** Purple Fiddle (96 East Ave; deli food, live music, hostel upstairs), TipTop (coffee and baked goods in the morning, burgers at night), Mountain State Brewing (flatbreads), Happy & More Bakery ([WV Tourism](https://wvtourism.com/craft-brew-town-thomas-davis/), [Only In Your State](https://www.onlyinyourstate.com/trip-ideas/west-virginia/walkable-town-day-trip-wv)).
- **Davis (Fri mi 51).** Sirianni's Café (474 William Ave, cash only per a 2020 review), Blackwater Brewing, Stumptown Ales, Sawmill Restaurant. Hellbender Burritos was reopening under new owners in 2026 but is unconfirmed ([The DA](https://www.thedaonline.com/culture/food/leftovers-scarce-from-sirianni-s-caf-in-davis/article_76f2a91e-3d6e-11ea-a8f5-cf3db10bac49.html), [Country Roads](https://countryroads.substack.com/p/hellbender-burritos-has-new-owners?open=false), [Coolworks](https://www.coolworks.com/hellbender-burritos/profile)).
- **Gaps.**
  - Sat: no confirmed food after Davis. The route passes about 1 mi from Canaan Valley State Park and the resort area around Sat mi 10–22, but that wasn't researched. Then nothing until the car at Alpena.
  - Sun: no food on route. Durbin has two restaurants (Big Al's, Station 2), but they are about 4 mi south of the Burner turn, off route.

## Findings and open questions

- **FR 209 is not on either route.** FR 209 starts off US-250 southeast of Huttonsville, near Cheat Bridge, and runs ~5 mi to Stonecoal Dispersed at about 3,500 ft on upper Shavers Fork.
  - Neither track reaches US-250. Canaan's southernmost point is 38.893°N near Alpena.
  - Canaan does ride the Shavers Fork valley, but only the lower stretch, north from Stuart/Bowden to Parsons at 2,100–1,700 ft, about 20 mi downstream of FR 209.
  - The posted construction closure was for the Red Run bridge. FR 209 and Stonecoal reopened **2025-08-14** ([USFS release](https://www.fs.usda.gov/r09/monongahela/newsroom/releases/forest-road-209-stonecoal-dispersed-camp-site-reopen-august-14-0), [Parsons Advocate](https://parsonsadvocate.com/news/pa-local-stories/forest-road-209-to-stonecoal-dispersed-camp-site-to-reopen-august-14-2025/)). If a closure is posted now, it is a new one; check MNF alerts.
- **Fri night: Canaan Loop Rd dispersed camping** (decided 2026-10-17, Brandon's call). Blackwater Falls SP campground was ~$50/night with one spot left. Dispersed camping is not allowed around Parsons–Thomas–Davis (mixed and private land), so the plan is to eat and fill water in Davis, then ride ~6 mi through the state park onto Canaan Loop Rd (FR 13). Once onX shows Monongahela NF land, camp 100+ ft off the road. Campendium lists at least seven established free sites along the road, and the best ones with fire rings are east of the Pointy Knob trailhead (likely too far for Friday). No toilets or water. Backups: Blackwater Falls SP, Canaan Valley SP, or a motel in Davis/Thomas.
- **Sat night at the car.** Bear Heaven is a drive-up campground 4.3 mi from the lot, so the easy move is to drive the car up for the night and back down Sunday. Gladwin (Sat mi 31.4) works as a backup, but it puts Sunday at ~69 mi.
- **Sunday is long.** The ride is 55.7 mi, then the drive back to Dayton is ~4.5 h. Consider an early start, or leave the Little River camps for a later trip.
- **Water.** On West Fork the hand pump is the only treated water (Sun mi 34.5). Bear Heaven has none. Filter everything else.
- **Navigation.** Most of the route has no cell service. Download offline maps in onX and RWGPS before leaving Dayton.
- **Season.** On today's date (October) archery deer season is open in WV, so wear some blaze orange. Bear Heaven closes for the season after November.
- **Not verified.** The exact Alpena lot, and the coordinates for Lower Glady and FR 44, are user-submitted on third-party sites. Web fetches of USFS/WVU pages were blocked from the research sandbox, so the facts above come from search-result summaries.

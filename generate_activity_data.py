"""
Generates all 64 outdoor_activity_data/*.json files for Breezeplan.
Each file is an array of activity objects appropriate for the given
(group_size, temperature, time_range) combination.

Run from the project root:
    python generate_activity_data.py
"""

import json
import os

# ─── Master activity library ───────────────────────────────────────────────
# Each entry carries:
#   temp_ok   – list of temp categories the activity suits
#   time_ok   – list of time-range categories the activity suits
#   group_ok  – list of group-size categories the activity suits
#   + all fields the frontend needs

ACTIVITIES = [
    {
        "id": 1,
        "activity": "Jogging",
        "description": "A refreshing jog along the scenic Aasee lake path, ideal for clearing your head.",
        "groupSuitability": "Best for individuals or couples",
        "timeRequired": "20–45 min",
        "image": "https://images.unsplash.com/photo-1571008887538-b36bb32f4571?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Aasee Lake Trail",
            "lighting": "Well-lit path along the lake",
            "description": "A 7 km paved ring around the Aasee lake, flat and popular with joggers year-round.",
            "redirectUrl": "https://maps.google.com/?q=Aasee+Münster",
            "safetyTips": ["Watch for cyclists sharing the path", "Wear reflective gear in low light", "Stay hydrated"]
        },
        "temp_ok": ["mild", "warm"],
        "time_ok": ["short", "moderate"],
        "group_ok": ["single", "couple"],
    },
    {
        "id": 2,
        "activity": "Cycling",
        "description": "Explore Münster on two wheels along its famous Promenade ring or riverside paths.",
        "groupSuitability": "Suitable for all group sizes",
        "timeRequired": "45–90 min",
        "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Münster Promenade Ring",
            "lighting": "Well-lit tree-lined boulevard",
            "description": "A 4.5 km tree-lined ring encircling the old city, beloved by cyclists and pedestrians alike.",
            "redirectUrl": "https://maps.google.com/?q=Promenade+Münster",
            "safetyTips": ["Yield to pedestrians", "Follow cycling direction signs", "Lock bikes at official stands"]
        },
        "temp_ok": ["cold", "mild", "warm"],
        "time_ok": ["moderate", "long", "extended"],
        "group_ok": ["single", "couple", "small_group", "large_group"],
    },
    {
        "id": 3,
        "activity": "Hiking",
        "description": "Trek through forested trails on the outskirts of Münster and breathe in the fresh air.",
        "groupSuitability": "Great for individuals, couples, or small groups",
        "timeRequired": "90–150 min",
        "image": "https://images.unsplash.com/photo-1551632811-561732d1e306?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Sentruper Höhe Forest Trails",
            "lighting": "Low lighting under tree canopy — bring a torch in winter",
            "description": "A network of well-marked trails through mixed woodland on the western edge of Münster.",
            "redirectUrl": "https://maps.google.com/?q=Sentruper+Höhe+Münster",
            "safetyTips": ["Wear sturdy footwear", "Inform someone of your route", "Carry a charged mobile phone"]
        },
        "temp_ok": ["cold", "mild", "warm"],
        "time_ok": ["long", "extended"],
        "group_ok": ["single", "couple", "small_group"],
    },
    {
        "id": 4,
        "activity": "Outdoor Yoga",
        "description": "Start your day with a calming yoga session surrounded by the palace gardens.",
        "groupSuitability": "Suitable for individuals or groups up to 6",
        "timeRequired": "30–60 min",
        "image": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Schloss Garden (University Palace Gardens)",
            "lighting": "Open and sunny during daytime",
            "description": "The elegant baroque palace gardens of Münster University — flat lawns perfect for yoga mats.",
            "redirectUrl": "https://maps.google.com/?q=Schloss+Münster",
            "safetyTips": ["Bring your own mat", "Be respectful of other visitors", "Check garden opening hours"]
        },
        "temp_ok": ["mild", "warm"],
        "time_ok": ["short", "moderate"],
        "group_ok": ["single", "couple", "small_group"],
    },
    {
        "id": 5,
        "activity": "Picnic",
        "description": "Relax on the grass with good food and great company in one of Münster's green spaces.",
        "groupSuitability": "Perfect for couples, families, and small groups",
        "timeRequired": "60–120 min",
        "image": "https://images.unsplash.com/photo-1594608661623-aa0bd3a69d98?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Westpark Münster",
            "lighting": "Open parkland — good natural light",
            "description": "A spacious park in western Münster with wide meadows, ideal for picnics and relaxation.",
            "redirectUrl": "https://maps.google.com/?q=Westpark+Münster",
            "safetyTips": ["Take your litter home", "Keep noise levels considerate", "Avoid areas with bees and wasps near food"]
        },
        "temp_ok": ["mild", "warm", "hot"],
        "time_ok": ["moderate", "long"],
        "group_ok": ["couple", "small_group", "large_group"],
    },
    {
        "id": 6,
        "activity": "Frisbee",
        "description": "Toss a frisbee with friends on the open grass of Gievenbeck Park.",
        "groupSuitability": "Best for pairs or small groups",
        "timeRequired": "30–60 min",
        "image": "https://images.unsplash.com/photo-1606092195730-5d7b9af1efc5?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Gievenbeck Sports Park",
            "lighting": "Open meadow — good light in daytime",
            "description": "A residential sports park with large open grass areas suitable for informal games.",
            "redirectUrl": "https://maps.google.com/?q=Gievenbeck+Münster",
            "safetyTips": ["Be aware of nearby pedestrians", "Avoid throwing near dog walkers", "Use soft discs for beginners"]
        },
        "temp_ok": ["mild", "warm"],
        "time_ok": ["short", "moderate"],
        "group_ok": ["couple", "small_group", "large_group"],
    },
    {
        "id": 7,
        "activity": "Soccer",
        "description": "Organise a casual kick-about on one of Münster's public sports fields.",
        "groupSuitability": "Best for teams of 6–12 people",
        "timeRequired": "60–120 min",
        "image": "https://images.unsplash.com/photo-1599058918144-1ffabb351dce?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Gievenbeck Sports Grounds",
            "lighting": "Floodlit pitches available in evenings",
            "description": "Public football pitches with marked fields — first come, first served.",
            "redirectUrl": "https://maps.google.com/?q=Gievenbeck+Sportplatz+Münster",
            "safetyTips": ["Warm up before play", "Bring plenty of water", "Check pitch availability during busy periods"]
        },
        "temp_ok": ["mild", "warm", "cold"],
        "time_ok": ["moderate", "long", "extended"],
        "group_ok": ["small_group", "large_group"],
    },
    {
        "id": 8,
        "activity": "Bird Watching",
        "description": "Spot a variety of bird species around the reed beds and shores of the Aasee lake.",
        "groupSuitability": "Ideal for individuals or couples",
        "timeRequired": "30–60 min",
        "image": "https://images.unsplash.com/photo-1552727131-5fc6af2b0ae4?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Aasee Lakeside Nature Area",
            "lighting": "Open lakeside — best at dawn and dusk",
            "description": "The reed beds on the south bank of Aasee are a haven for waterfowl, herons, and migratory birds.",
            "redirectUrl": "https://maps.google.com/?q=Aasee+Südseite+Münster",
            "safetyTips": ["Keep noise to a minimum", "Don't disturb nesting areas", "Binoculars recommended"]
        },
        "temp_ok": ["cold", "mild"],
        "time_ok": ["short", "moderate"],
        "group_ok": ["single", "couple"],
    },
    {
        "id": 9,
        "activity": "Photography Walk",
        "description": "Capture stunning urban and nature shots on a guided self-tour of Münster's most photogenic spots.",
        "groupSuitability": "Perfect for solo explorers or pairs",
        "timeRequired": "45–90 min",
        "image": "https://images.unsplash.com/photo-1452587925148-ce544e77e70d?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Münster Old City & Promenade",
            "lighting": "Best in golden hour (early morning or late afternoon)",
            "description": "From the Lambertikirche to the Promenade elm trees, Münster offers countless photogenic corners.",
            "redirectUrl": "https://maps.google.com/?q=Lambertikirche+Münster",
            "safetyTips": ["Be respectful when photographing people", "Watch your step on cobblestones", "Keep equipment secure in crowds"]
        },
        "temp_ok": ["cold", "mild", "warm"],
        "time_ok": ["short", "moderate"],
        "group_ok": ["single", "couple"],
    },
    {
        "id": 10,
        "activity": "Ice Skating",
        "description": "Glide on the ice at Münster's main rink — great fun for all abilities in the winter months.",
        "groupSuitability": "Suitable for individuals, couples, and small groups",
        "timeRequired": "60–90 min",
        "image": "https://images.unsplash.com/photo-1548777123-e216912df7d8?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Eishalle Münster",
            "lighting": "Fully lit indoor facility",
            "description": "Münster's indoor ice rink offering public skating sessions throughout the winter season.",
            "redirectUrl": "https://maps.google.com/?q=Eishalle+Münster",
            "safetyTips": ["Wear proper ankle-supporting skates", "Beginners should use rink aids", "Helmets recommended for children"]
        },
        "temp_ok": ["cold"],
        "time_ok": ["moderate", "long"],
        "group_ok": ["single", "couple", "small_group"],
    },
    {
        "id": 11,
        "activity": "Sledding",
        "description": "When snow falls, head to the gentle slopes near Münster for exhilarating sledding runs.",
        "groupSuitability": "Fun for all group sizes",
        "timeRequired": "30–60 min",
        "image": "https://images.unsplash.com/photo-1511702771955-48b4c7370602?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Hügel am Preußenstadion",
            "lighting": "Open area — good natural light in daytime",
            "description": "A natural slope near the stadium that transforms into a popular sledding hill after snowfall.",
            "redirectUrl": "https://maps.google.com/?q=Preußenstadion+Münster",
            "safetyTips": ["Check slope for obstacles before sledding", "Children must be supervised", "Avoid icy patches — walk carefully"]
        },
        "temp_ok": ["cold"],
        "time_ok": ["short", "moderate"],
        "group_ok": ["single", "couple", "small_group", "large_group"],
    },
    {
        "id": 12,
        "activity": "Winter Photography",
        "description": "Capture the city's frosty beauty — mist on the Aasee, frost-dusted trees in the Schloss garden.",
        "groupSuitability": "Best for individuals or couples",
        "timeRequired": "30–75 min",
        "image": "https://images.unsplash.com/photo-1516912481808-3406841bd33c?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Schloss Garden & Aasee Viewpoints",
            "lighting": "Low winter light — ideal for moody shots",
            "description": "Cold mornings create stunning fog over the Aasee and frost on the baroque Schloss garden hedgerows.",
            "redirectUrl": "https://maps.google.com/?q=Schloss+Münster",
            "safetyTips": ["Dress in warm layers", "Protect camera from moisture", "Watch for icy paths"]
        },
        "temp_ok": ["cold"],
        "time_ok": ["short", "moderate"],
        "group_ok": ["single", "couple"],
    },
    {
        "id": 13,
        "activity": "Nordic Walking",
        "description": "A low-impact full-body workout using poles along Münster's flat trails.",
        "groupSuitability": "Suitable for individuals or small groups",
        "timeRequired": "45–90 min",
        "image": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Promenade & Aasee Ring",
            "lighting": "Well-lit paths suitable for early mornings",
            "description": "Flat, paved routes with minimal traffic — ideal for Nordic walking technique.",
            "redirectUrl": "https://maps.google.com/?q=Promenade+Münster",
            "safetyTips": ["Use rubber tips on poles to protect pavement", "Yield to cyclists", "Warm up wrists and shoulders first"]
        },
        "temp_ok": ["cold", "mild"],
        "time_ok": ["moderate", "long"],
        "group_ok": ["single", "couple", "small_group"],
    },
    {
        "id": 14,
        "activity": "Cross-Country Skiing",
        "description": "On rare snowy days, the fields around Münster become a cross-country skiing paradise.",
        "groupSuitability": "Best for individuals or couples",
        "timeRequired": "2–4 hours",
        "image": "https://images.unsplash.com/photo-1548438294-1ad5d5f4f063?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Rüschhaus Estate Fields",
            "lighting": "Open countryside — natural light only",
            "description": "When snow covers the historic Rüschhaus estate, flat fields provide great cross-country skiing loops.",
            "redirectUrl": "https://maps.google.com/?q=Rüschhaus+Münster",
            "safetyTips": ["Only attempt after significant snowfall", "Inform someone of your route", "Bring emergency supplies"]
        },
        "temp_ok": ["cold"],
        "time_ok": ["long", "extended"],
        "group_ok": ["single", "couple"],
    },
    {
        "id": 15,
        "activity": "Kayaking",
        "description": "Paddle across the calm waters of the Aasee lake and discover a tranquil side of Münster.",
        "groupSuitability": "Great for couples or small groups",
        "timeRequired": "60–120 min",
        "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Aasee Lake Rental Point",
            "lighting": "Open water — good visibility in daylight",
            "description": "Kayak and canoe rentals available at the Aasee boathouse. Calm waters and scenic shores.",
            "redirectUrl": "https://maps.google.com/?q=Aasee+Bootsverleih+Münster",
            "safetyTips": ["Wear a life jacket at all times", "Avoid the middle channel used by sailing boats", "Check weather before heading out"]
        },
        "temp_ok": ["mild", "warm"],
        "time_ok": ["moderate", "long"],
        "group_ok": ["couple", "small_group"],
    },
    {
        "id": 16,
        "activity": "Stand-Up Paddleboarding",
        "description": "Test your balance and core strength on a stand-up paddleboard on the Aasee.",
        "groupSuitability": "Suitable for individuals or couples",
        "timeRequired": "45–90 min",
        "image": "https://images.unsplash.com/photo-1559829099-8d54ef4b22e4?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Aasee Lake — South Shore",
            "lighting": "Open water with good natural light",
            "description": "The calm, shallow waters near the Aasee south shore are ideal for paddleboarding beginners.",
            "redirectUrl": "https://maps.google.com/?q=Aasee+Südseite+Münster",
            "safetyTips": ["Wear a leash and life jacket", "Avoid strong wind conditions", "Stay within the designated area"]
        },
        "temp_ok": ["warm", "hot"],
        "time_ok": ["moderate", "long"],
        "group_ok": ["single", "couple"],
    },
    {
        "id": 17,
        "activity": "Swimming",
        "description": "Cool off on a hot day at one of Münster's outdoor swimming facilities.",
        "groupSuitability": "Suitable for all group sizes",
        "timeRequired": "60–120 min",
        "image": "https://images.unsplash.com/photo-1530549387789-4c1017266635?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Freibad Coburg (Münster Outdoor Pool)",
            "lighting": "Open outdoor facility — sunlit",
            "description": "Münster's main outdoor pool with multiple swimming lanes, slides, and sunbathing areas.",
            "redirectUrl": "https://maps.google.com/?q=Freibad+Coburg+Münster",
            "safetyTips": ["Follow lifeguard instructions", "Apply sunscreen generously", "Never swim alone in open water"]
        },
        "temp_ok": ["hot", "warm"],
        "time_ok": ["moderate", "long"],
        "group_ok": ["single", "couple", "small_group", "large_group"],
    },
    {
        "id": 18,
        "activity": "Trail Running",
        "description": "Push your limits on the wooded trails of Sentruper Höhe — a favourite with Münster's runners.",
        "groupSuitability": "Best for individuals or small groups",
        "timeRequired": "45–90 min",
        "image": "https://images.unsplash.com/photo-1527956041665-d7a1b380c460?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Sentruper Höhe Trail Network",
            "lighting": "Shaded forest paths — bring a headtorch for dawn/dusk",
            "description": "Undulating trails through birch and oak woodland — a refreshing change from city pavement.",
            "redirectUrl": "https://maps.google.com/?q=Sentruper+Höhe+Münster",
            "safetyTips": ["Wear trail shoes", "Carry water", "Tell someone your route and expected return time"]
        },
        "temp_ok": ["mild", "warm"],
        "time_ok": ["moderate", "long"],
        "group_ok": ["single", "couple", "small_group"],
    },
    {
        "id": 19,
        "activity": "Rock Climbing (Indoor)",
        "description": "Tackle bouldering walls and roped routes at Münster's climbing gym — great year-round.",
        "groupSuitability": "Suitable for individuals, couples, and small groups",
        "timeRequired": "90–180 min",
        "image": "https://images.unsplash.com/photo-1522163182402-834f871fd851?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "High East Bouldering Gym, Münster",
            "lighting": "Fully lit indoor facility",
            "description": "Modern bouldering and lead-climbing walls suitable for all skill levels, from complete beginners to advanced climbers.",
            "redirectUrl": "https://maps.google.com/?q=Kletterhalle+Münster",
            "safetyTips": ["Complete safety briefing before first visit", "Wear appropriate climbing shoes", "Spot your partner on bouldering walls"]
        },
        "temp_ok": ["cold", "mild", "warm", "hot"],
        "time_ok": ["long", "extended"],
        "group_ok": ["single", "couple", "small_group"],
    },
    {
        "id": 20,
        "activity": "Geocaching",
        "description": "Use GPS to hunt for hidden caches scattered around Münster's parks and landmarks.",
        "groupSuitability": "Fun for all group sizes",
        "timeRequired": "60–180 min",
        "image": "https://images.unsplash.com/photo-1595079676339-1534801ad6cf?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Münster City & Surroundings",
            "lighting": "Varies by cache location — most are accessible in daylight",
            "description": "Hundreds of geocaches hidden across Münster — from the city centre to forests and cycle paths.",
            "redirectUrl": "https://maps.google.com/?q=Münster+city+centre",
            "safetyTips": ["Download the Geocaching app before you go", "Respect private property", "Return the cache exactly as found"]
        },
        "temp_ok": ["cold", "mild", "warm"],
        "time_ok": ["moderate", "long", "extended"],
        "group_ok": ["single", "couple", "small_group", "large_group"],
    },
    {
        "id": 21,
        "activity": "Orienteering",
        "description": "Navigate using a map and compass through the forests around Münster in a self-timed challenge.",
        "groupSuitability": "Best for individuals or small groups",
        "timeRequired": "90–150 min",
        "image": "https://images.unsplash.com/photo-1452421822248-d4c2b47f0c81?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Roxel Forest Orienteering Course",
            "lighting": "Low in dense sections — not recommended after dark",
            "description": "A dedicated orienteering area west of Münster with control points marked on specialist maps.",
            "redirectUrl": "https://maps.google.com/?q=Wald+Roxel+Münster",
            "safetyTips": ["Carry a whistle and first aid kit", "Don't stray beyond marked boundaries", "Buddy system recommended for beginners"]
        },
        "temp_ok": ["cold", "mild"],
        "time_ok": ["long", "extended"],
        "group_ok": ["single", "couple", "small_group"],
    },
    {
        "id": 22,
        "activity": "Skateboarding",
        "description": "Practice tricks and cruise around Münster's popular skate park near the Aasee.",
        "groupSuitability": "Great for individuals or small groups",
        "timeRequired": "45–90 min",
        "image": "https://images.unsplash.com/photo-1547447134-cd3f5c716030?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Skatepark Münster (near Aasee)",
            "lighting": "Partially lit — best in daytime",
            "description": "A well-maintained skate park with bowls, rails, and flat sections for all skill levels.",
            "redirectUrl": "https://maps.google.com/?q=Skatepark+Münster+Aasee",
            "safetyTips": ["Wear a helmet and pads", "Respect right-of-way on shared obstacles", "Keep the area tidy"]
        },
        "temp_ok": ["mild", "warm"],
        "time_ok": ["short", "moderate"],
        "group_ok": ["single", "couple", "small_group"],
    },
    {
        "id": 23,
        "activity": "Beach Volleyball",
        "description": "Spike, set, and serve on Münster's sandy beach volleyball courts by the Aasee.",
        "groupSuitability": "Best for teams of 4–8 people",
        "timeRequired": "60–120 min",
        "image": "https://images.unsplash.com/photo-1612872087720-bb876e2e67d1?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Aasee Beach Volleyball Courts",
            "lighting": "Open outdoor courts — daylight hours only",
            "description": "Official sand courts on the Aasee lakeside, bookable or first-come-first-served in summer.",
            "redirectUrl": "https://maps.google.com/?q=Beachvolleyball+Aasee+Münster",
            "safetyTips": ["Check court availability before travelling", "Apply sunscreen in summer", "Bring enough water for the team"]
        },
        "temp_ok": ["warm", "hot"],
        "time_ok": ["moderate", "long"],
        "group_ok": ["small_group", "large_group"],
    },
    {
        "id": 24,
        "activity": "Kite Flying",
        "description": "Let your kite soar on the wide open meadows of Westpark — perfect when it's breezy.",
        "groupSuitability": "Fun for all group sizes",
        "timeRequired": "30–60 min",
        "image": "https://images.unsplash.com/photo-1507608869274-d3177c8bb4c7?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Westpark Open Meadow",
            "lighting": "Open parkland with good natural light",
            "description": "Wide, flat meadows with minimal obstacles — ideal conditions for getting a kite up quickly.",
            "redirectUrl": "https://maps.google.com/?q=Westpark+Münster",
            "safetyTips": ["Avoid flying near power lines or trees", "Keep children away from kite lines", "Lower the kite in thunderstorms"]
        },
        "temp_ok": ["mild", "warm"],
        "time_ok": ["short", "moderate"],
        "group_ok": ["single", "couple", "small_group", "large_group"],
    },
    {
        "id": 25,
        "activity": "Nature Walk",
        "description": "A gentle stroll through quiet woodland and fields, soaking up the natural surroundings.",
        "groupSuitability": "Suitable for all group sizes",
        "timeRequired": "45–90 min",
        "image": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Rieselfelder Münster Nature Reserve",
            "lighting": "Open reserve — good natural light in daytime",
            "description": "A UNESCO-recognised wetland reserve north of Münster, home to rare birds and wildflowers.",
            "redirectUrl": "https://maps.google.com/?q=Rieselfelder+Münster",
            "safetyTips": ["Stick to marked paths to protect nesting wildlife", "No dogs in the reserve", "Bring binoculars for wildlife spotting"]
        },
        "temp_ok": ["cold", "mild", "warm"],
        "time_ok": ["moderate", "long"],
        "group_ok": ["single", "couple", "small_group", "large_group"],
    },
    {
        "id": 26,
        "activity": "Team Scavenger Hunt",
        "description": "Race through Münster solving clues at landmarks — a classic team-building adventure.",
        "groupSuitability": "Best for groups of 6 or more",
        "timeRequired": "90–180 min",
        "image": "https://images.unsplash.com/photo-1607627000458-210e8197b2f0?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Münster City Centre",
            "lighting": "Well-lit city streets and squares",
            "description": "Create a route linking the Prinzipalmarkt, Dom, Lambertikirche, and Rathaus for a fun city-wide hunt.",
            "redirectUrl": "https://maps.google.com/?q=Prinzipalmarkt+Münster",
            "safetyTips": ["Agree meeting points in advance", "Keep groups together in busy areas", "Carry a city map as backup"]
        },
        "temp_ok": ["cold", "mild", "warm"],
        "time_ok": ["long", "extended"],
        "group_ok": ["small_group", "large_group"],
    },
    {
        "id": 27,
        "activity": "Outdoor BBQ",
        "description": "Fire up the grill in one of Münster's designated BBQ areas for a relaxed outdoor meal.",
        "groupSuitability": "Perfect for groups of any size",
        "timeRequired": "2–4 hours",
        "image": "https://images.unsplash.com/photo-1529543544282-ea669407fca3?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Westpark BBQ Area",
            "lighting": "Open park — good afternoon light",
            "description": "Westpark has designated BBQ zones with bins and benches — arrive early to secure a spot in summer.",
            "redirectUrl": "https://maps.google.com/?q=Westpark+Münster",
            "safetyTips": ["Use designated BBQ zones only", "Never leave the grill unattended", "Extinguish coals fully before leaving"]
        },
        "temp_ok": ["warm", "hot"],
        "time_ok": ["long", "extended"],
        "group_ok": ["couple", "small_group", "large_group"],
    },
    {
        "id": 28,
        "activity": "Stargazing",
        "description": "Escape city light pollution and gaze at the night sky from the countryside near Münster.",
        "groupSuitability": "Ideal for individuals or couples",
        "timeRequired": "60–120 min",
        "image": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Rüschhaus Estate Fields",
            "lighting": "Dark skies — no artificial lighting",
            "description": "The flat open fields around the Rüschhaus estate offer some of the darkest skies near Münster.",
            "redirectUrl": "https://maps.google.com/?q=Rüschhaus+Münster",
            "safetyTips": ["Bring warm layers — it gets cold quickly at night", "Use red-light torches to preserve night vision", "Inform someone where you're going"]
        },
        "temp_ok": ["cold", "mild"],
        "time_ok": ["long", "extended"],
        "group_ok": ["single", "couple"],
    },
    {
        "id": 29,
        "activity": "Zoo Visit",
        "description": "Spend the day at the award-winning Allwetterzoo Münster — one of Germany's best all-weather zoos.",
        "groupSuitability": "Great for families and groups of all sizes",
        "timeRequired": "2–4 hours",
        "image": "https://images.unsplash.com/photo-1534567153574-2b12153a87f0?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Allwetterzoo Münster",
            "lighting": "Well-lit covered and outdoor areas",
            "description": "A large all-weather zoo with covered walkways — enjoyable rain or shine, with over 300 animal species.",
            "redirectUrl": "https://maps.google.com/?q=Allwetterzoo+Münster",
            "safetyTips": ["Follow all zoo safety guidelines", "Don't feed the animals", "Keep children within sight at all times"]
        },
        "temp_ok": ["cold", "mild", "warm", "hot"],
        "time_ok": ["long", "extended"],
        "group_ok": ["couple", "small_group", "large_group"],
    },
    {
        "id": 30,
        "activity": "Morning Walk",
        "description": "Start your day with a gentle morning walk along the canal paths and lakeside promenade.",
        "groupSuitability": "Perfect for individuals or couples",
        "timeRequired": "15–30 min",
        "image": "https://images.unsplash.com/photo-1476611338391-6f395a0ebc7b?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Dortmund-Ems Canal Towpath",
            "lighting": "Open towpath — good light from early morning",
            "description": "A flat, traffic-free canal towpath stretching several kilometres north of Münster city centre.",
            "redirectUrl": "https://maps.google.com/?q=Dortmund-Ems+Kanal+Münster",
            "safetyTips": ["Watch for cyclists on the shared path", "Wear layers — mornings can be chilly", "Keep dogs on leads near water"]
        },
        "temp_ok": ["cold", "mild", "warm", "hot"],
        "time_ok": ["short"],
        "group_ok": ["single", "couple"],
    },
    {
        "id": 31,
        "activity": "Park Workout",
        "description": "Use the outdoor fitness equipment along the Promenade for a free, equipment-led workout.",
        "groupSuitability": "Best for individuals or couples",
        "timeRequired": "20–45 min",
        "image": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Promenade Fitness Trail",
            "lighting": "Well-lit boulevard",
            "description": "Outdoor gym stations installed along the Promenade — free to use, suitable for all fitness levels.",
            "redirectUrl": "https://maps.google.com/?q=Promenade+Münster",
            "safetyTips": ["Warm up before using equipment", "Wipe down equipment after use", "Respect other users' space"]
        },
        "temp_ok": ["mild", "warm"],
        "time_ok": ["short", "moderate"],
        "group_ok": ["single", "couple"],
    },
    {
        "id": 32,
        "activity": "Casual Football",
        "description": "Kick a ball around with friends for a fun, low-key game on the public fields.",
        "groupSuitability": "Best for small and large groups",
        "timeRequired": "45–75 min",
        "image": "https://images.unsplash.com/photo-1553778263-73a83bab9b0c?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Westpark Meadow & Sports Field",
            "lighting": "Open meadow — good during daylight",
            "description": "Large open grass areas in Westpark often used for informal football games — no booking required.",
            "redirectUrl": "https://maps.google.com/?q=Westpark+Münster",
            "safetyTips": ["Be mindful of other park users", "No slide tackles on hard ground", "Carry a basic first aid kit"]
        },
        "temp_ok": ["mild", "warm", "cold"],
        "time_ok": ["moderate", "long"],
        "group_ok": ["small_group", "large_group"],
    },
    {
        "id": 33,
        "activity": "Sunset Walk",
        "description": "Stroll along the harbour or lakeside to enjoy Münster's evening golden hour.",
        "groupSuitability": "Wonderful for all group sizes",
        "timeRequired": "20–40 min",
        "image": "https://images.unsplash.com/photo-1475552113915-6fcb52652ba2?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Münster Harbour (Hafen)",
            "lighting": "Well-lit urban waterfront",
            "description": "The converted industrial harbour is Münster's trendiest evening destination — cafes, art, and waterside views.",
            "redirectUrl": "https://maps.google.com/?q=Hafen+Münster",
            "safetyTips": ["Stay on the designated pedestrian areas", "Watch children near the water edge", "Busy at weekends — allow extra time"]
        },
        "temp_ok": ["mild", "warm", "hot"],
        "time_ok": ["short"],
        "group_ok": ["single", "couple", "small_group", "large_group"],
    },
    {
        "id": 34,
        "activity": "Group Cycling Tour",
        "description": "Organise a group ride exploring the cycling routes around Münster and into the countryside.",
        "groupSuitability": "Great for small and large groups",
        "timeRequired": "2–4 hours",
        "image": "https://images.unsplash.com/photo-1541625602330-2277a4c46182?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Münster–Telgte Cycle Route",
            "lighting": "Mix of lit urban and unlit rural sections",
            "description": "A popular 20 km round trip from Münster to the pilgrimage town of Telgte along marked cycle paths.",
            "redirectUrl": "https://maps.google.com/?q=Münster+Telgte+Fahrradweg",
            "safetyTips": ["Ensure all bikes are roadworthy before departure", "Agree a pace suitable for the slowest rider", "Carry a puncture repair kit"]
        },
        "temp_ok": ["mild", "warm"],
        "time_ok": ["long", "extended"],
        "group_ok": ["small_group", "large_group"],
    },
    {
        "id": 35,
        "activity": "Outdoor Winter Market Visit",
        "description": "Browse stalls, sip Glühwein, and enjoy the festive atmosphere of Münster's winter market.",
        "groupSuitability": "Fun for all group sizes",
        "timeRequired": "30–90 min",
        "image": "https://images.unsplash.com/photo-1512909006721-3d6018887383?w=600",
        "locationInfo": {
            "pathNameOrLocationName": "Münster Christmas Market, Prinzipalmarkt",
            "lighting": "Beautifully lit with market stalls",
            "description": "One of Germany's most charming Christmas markets, set against the historic gabled townhouses of the Prinzipalmarkt.",
            "redirectUrl": "https://maps.google.com/?q=Weihnachtsmarkt+Münster+Prinzipalmarkt",
            "safetyTips": ["Keep bags close in crowded areas", "Be aware of open fire hazards near stalls", "Dress warmly — market is outdoors"]
        },
        "temp_ok": ["cold"],
        "time_ok": ["short", "moderate", "long"],
        "group_ok": ["single", "couple", "small_group", "large_group"],
    },
]

# ─── Category mappings ──────────────────────────────────────────────────────

GROUP_SIZES  = ["single", "couple", "small_group", "large_group"]
TEMPERATURES = ["cold", "mild", "warm", "hot"]
TIME_RANGES  = ["short", "moderate", "long", "extended"]

# Minimum activities to include per file; if fewer match we fall back to adding
# the closest-fitting extras so every file always has ≥ 6 entries.
MIN_ACTIVITIES = 6

# ─── Selector ──────────────────────────────────────────────────────────────

def select_activities(group, temp, time_range):
    """Return a list of activity dicts appropriate for the given combination."""
    # Primary: all three tags match
    primary = [
        a for a in ACTIVITIES
        if group in a["group_ok"]
        and temp in a["temp_ok"]
        and time_range in a["time_ok"]
    ]

    if len(primary) >= MIN_ACTIVITIES:
        return primary

    # Secondary: at least two tags match (temp + group preferred)
    secondary = [
        a for a in ACTIVITIES
        if a not in primary
        and group in a["group_ok"]
        and temp in a["temp_ok"]
    ]
    combined = primary + secondary
    if len(combined) >= MIN_ACTIVITIES:
        return combined[:MIN_ACTIVITIES + 2]  # a couple extra for RL variety

    # Tertiary: group matches (any temp/time)
    tertiary = [
        a for a in ACTIVITIES
        if a not in combined and group in a["group_ok"]
    ]
    combined = (combined + tertiary)[:MIN_ACTIVITIES + 2]
    return combined if combined else ACTIVITIES[:MIN_ACTIVITIES]


def clean_activity(a, idx):
    """Return a copy of the activity dict without the filtering-only tag keys."""
    return {
        "id": idx + 1,
        "activity": a["activity"],
        "description": a["description"],
        "groupSuitability": a["groupSuitability"],
        "timeRequired": a["timeRequired"],
        "image": a["image"],
        "locationInfo": a["locationInfo"],
    }


# ─── Generator ─────────────────────────────────────────────────────────────

def generate_all_files():
    output_dir = "outdoor_activity_data"
    os.makedirs(output_dir, exist_ok=True)

    total = 0
    for group in GROUP_SIZES:
        for temp in TEMPERATURES:
            for time_range in TIME_RANGES:
                activities = select_activities(group, temp, time_range)
                payload = [clean_activity(a, i) for i, a in enumerate(activities)]

                filename = f"outdoor_activity_{group}_{temp}_{time_range}.json"
                filepath = os.path.join(output_dir, filename)

                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(payload, f, indent=2, ensure_ascii=False)

                print(f"  OK {filename}  ({len(payload)} activities)")
                total += 1

    print(f"\nDone — {total} files written to '{output_dir}/'")


if __name__ == "__main__":
    generate_all_files()

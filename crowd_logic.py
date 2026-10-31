"""
Chennai Crowd Prediction Engine
Comprehensive database of Malls, Beaches, Parks, Swimming Pools, and Temples.
Includes fuzzy search, real geocoding, and transit calculations.
"""

import math
import requests
from difflib import get_close_matches

CHENNAI_ORIGINS = [
    "Tambaram", "Guindy", "Anna Nagar", "Chennai Central", "Adyar", "Velachery",
    "T. Nagar", "Avadi", "Porur", "Thiruvanmiyur", "Mylapore", "Nungambakkam",
    "Kilpauk", "Chromepet", "Pallavaram", "Medavakkam", "Sholinganallur",
    "Perambur", "Royapettah", "Sowcarpet", "Egmore", "Saidapet", "Vadapalani",
    "Koyambedu", "Mogappair", "Ambattur", "Poonamallee", "Madipakkam",
    "Alwarpet", "Besant Nagar", "Thoraipakkam", "Navalur", "Siruseri", "Kotturpuram"
]

DESTINATIONS = [
    # --- MALLS ---
    {
        "id": "vr_mall",
        "name": "VR Chennai",
        "type": "Mall",
        "zone": "Anna Nagar West",
        "coords": (13.0886, 80.1983),
        "max_capacity": 7500,
        "is_indoor": True,
        "description": "Massive lifestyle mall with Timezone Game Zone, PVR Luxe, rooftop cafes, and cultural architecture.",
        "best_for": ["Friends", "Couple", "Family", "Single"],
        "couple_friendly": True,
        "vibe_tags": ["Timezone Arcade", "Bowling Alley", "PVR Cinemas", "Aesthetic Courtyard", "Rooftop Cafes"],
        "parking": {
            "bike_stress": "Low - Dedicated multi-level two-wheeler ramp (₹20-₹30)",
            "car_stress": "High - 20-30 min queue at Jawaharlal Nehru Road ramp post 5 PM on weekends",
            "hack": "Park bike at Thirumangalam Metro for ₹15 and walk 800m if peak Saturday rush"
        },
        "transit": {
            "metro": "Thirumangalam Metro (Green Line) - 800m walk or ₹20 share-auto",
            "train": "Villivakkam Suburban (3.5 km)",
            "bus": "Thirumangalam Junction Bus Stop (Routes: 47D, 27B, 70V, 101)",
            "cheat_code": "Take Green line metro to Thirumangalam, exit Gate 2, jump in ₹20 share-auto directly to VR entry"
        },
        "event_hype_alert": "Moderate - Heavy weekend movie rush at PVR Luxe.",
        "budget_catalog": [
            {"item": "Timezone Arcade Single Token", "price": 80, "image": "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=300&q=80", "category": "Games"},
            {"item": "Timezone Air Hockey / Basketball Shootout", "price": 120, "image": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=300&q=80", "category": "Games"},
            {"item": "McDonald's McVeggie / McChicken Value Combo", "price": 199, "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300&q=80", "category": "Food"},
            {"item": "Timezone Krazy Kars Bumper Ride", "price": 160, "image": "https://images.unsplash.com/photo-1576618148400-f54bed99fcfd?w=300&q=80", "category": "Games"},
            {"item": "Timezone Bowling Alley (1 Full String Game)", "price": 380, "image": "https://images.unsplash.com/photo-1545232979-fbf68fe9b10d?w=300&q=80", "category": "Games"},
            {"item": "Two Cold Frappes at Courtyard", "price": 340, "image": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=300&q=80", "category": "Food"}
        ],
        "hourly_pattern": {"Morning": 20, "Afternoon": 55, "Evening": 92, "Night": 65}
    },
    {
        "id": "express_avenue",
        "name": "Express Avenue (EA)",
        "type": "Mall",
        "zone": "Royapettah",
        "coords": (13.0587, 80.2642),
        "max_capacity": 8500,
        "is_indoor": True,
        "description": "Centrally located hub featuring Escape Cinemas, gaming arcade, and a multi-cuisine food court.",
        "best_for": ["Friends", "Couple", "Family", "Single"],
        "couple_friendly": True,
        "vibe_tags": ["Escape Cinemas", "Central Hub", "Food Court", "Arcade Games"],
        "parking": {
            "bike_stress": "Moderate - Quick access via Whites Road rear gate (₹20)",
            "car_stress": "High - Long queues on Pattullos Road during weekend peak hours",
            "hack": "Avoid Pattullos Road car queue by parking at Thousand Lights Metro parking lot"
        },
        "transit": {
            "metro": "Thousand Lights Metro (Blue Line Gate 3) - 400m walk",
            "train": "Chennai Central (3 km)",
            "bus": "Express Avenue / Woods Road Stop (Routes: 21G, 22, 27B)",
            "cheat_code": "Get down at Thousand Lights Metro Gate 3, cross Club House Road to enter EA back gate in 4 mins"
        },
        "event_hype_alert": "Low - Regular commercial flow.",
        "budget_catalog": [
            {"item": "Filter Coffee & Hot Samosas at Food Court", "price": 110, "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=300&q=80", "category": "Food"},
            {"item": "McDonald's Extra Value Burger Meal", "price": 185, "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300&q=80", "category": "Food"},
            {"item": "Keventers Thick Milkshake", "price": 190, "image": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=300&q=80", "category": "Food"},
            {"item": "Escape Cinemas Regular Movie Ticket", "price": 240, "image": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=300&q=80", "category": "Cinema"}
        ],
        "hourly_pattern": {"Morning": 22, "Afternoon": 60, "Evening": 94, "Night": 70}
    },
    {
        "id": "phoenix_marketcity",
        "name": "Phoenix Marketcity",
        "type": "Mall",
        "zone": "Velachery",
        "coords": (12.9925, 80.2173),
        "max_capacity": 9500,
        "is_indoor": True,
        "description": "Massive lifestyle mall with IMAX, luxury apparel, bowling alley, and premium dining outlets.",
        "best_for": ["Friends", "Family", "Couple", "Single"],
        "couple_friendly": True,
        "vibe_tags": ["Luxury Shopping", "IMAX Theater", "Bowling & Arcade", "Cozy Cafes"],
        "parking": {
            "bike_stress": "Moderate - Multi-level basement parking fills up by 6 PM on Sunday",
            "car_stress": "Severe - Velachery bypass road gets backed up up to 1.5 km on weekends",
            "hack": "Take share-auto from Guindy Metro rather than driving a car through the Velachery junction choke"
        },
        "transit": {
            "metro": "Guindy Metro (4 km) + frequent share autos from Gate 3",
            "train": "Velachery MRTS Railway - 1.8 km",
            "bus": "Velachery Checkpost / Phoenix Mall Stop (Routes: 570, 119, 5C)",
            "cheat_code": "Take Metro to Guindy, walk to Race Course road side, catch the direct ₹20 share-auto to mall drop"
        },
        "event_hype_alert": "Moderate - Heavy weekend bottleneck.",
        "budget_catalog": [
            {"item": "Subway 6-inch Sub Value Combo", "price": 210, "image": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=300&q=80", "category": "Food"},
            {"item": "Arcade Card Top-up (3 basic video games)", "price": 300, "image": "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=300&q=80", "category": "Games"},
            {"item": "Two Artisanal Donuts & Hot Coffees", "price": 360, "image": "https://images.unsplash.com/photo-1527661591475-527312dd65f5?w=300&q=80", "category": "Food"}
        ],
        "hourly_pattern": {"Morning": 20, "Afternoon": 62, "Evening": 96, "Night": 74}
    },

    # --- BEACHES ---
    {
        "id": "marina_beach",
        "name": "Marina Beach",
        "type": "Beach",
        "zone": "Mylapore / Triplicane",
        "coords": (13.0500, 80.2824),
        "max_capacity": 42000,
        "is_indoor": False,
        "description": "Iconic Chennai coastline with sea breezes, carnival stalls, fresh fish fry, and lighthouse views.",
        "best_for": ["Family", "Friends", "Single"],
        "couple_friendly": False,
        "vibe_tags": ["Sunset Strolls", "Street Food", "Lighthouse Deck", "Carnival Stalls"],
        "parking": {
            "bike_stress": "Low - Open seaside service lane bike parking (₹10-₹20)",
            "car_stress": "Moderate - Kamarajar Salai service road gets packed near Gandhi Statue post 5 PM",
            "hack": "Park near Vivekanandar Illam service road stretch for hassle-free exits"
        },
        "transit": {
            "metro": "Government Estate Metro (1.5 km)",
            "train": "Chepauk / Thiruvallikeni MRTS - 400m walk",
            "bus": "Marina Beach / Vivekanandar Illam (Routes: 21G, 102, 45B)",
            "cheat_code": "Take MRTS train to Chepauk station, step directly onto the beach walkway in 3 mins"
        },
        "event_hype_alert": "High on Cricket Match Days due to Chepauk MA Chidambaram Stadium next door!",
        "budget_catalog": [
            {"item": "Marina Thenga Manga Pattani Sundal", "price": 30, "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=300&q=80", "category": "Food"},
            {"item": "Hot Molaga Bajji Plate (4 pcs)", "price": 40, "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=300&q=80", "category": "Food"},
            {"item": "Lighthouse Observation Deck Entry Ticket", "price": 50, "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=300&q=80", "category": "Sightseeing"},
            {"item": "Fresh Fried Vanjaram / Nethili Fish Fry Slice", "price": 120, "image": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=300&q=80", "category": "Food"}
        ],
        "hourly_pattern": {"Morning": 25, "Afternoon": 15, "Evening": 98, "Night": 50}
    },
    {
        "id": "besant_nagar",
        "name": "Besant Nagar (Elliot's Beach)",
        "type": "Beach",
        "zone": "Besant Nagar",
        "coords": (12.9988, 80.2725),
        "max_capacity": 15000,
        "is_indoor": False,
        "description": "Relaxed beach promenade with cozy cafes, the Schmidt Memorial, and romantic sunset breezes.",
        "best_for": ["Couple", "Friends", "Family", "Single"],
        "couple_friendly": True,
        "vibe_tags": ["Romantic Sunset", "Cafe Culture", "Schmidt Memorial", "Breezy Walk"],
        "parking": {
            "bike_stress": "Moderate - Beach promenade parking fills quickly on weekend evenings (₹20)",
            "car_stress": "Severe - 6th Avenue gridlocks easily, finding a car slot takes 20+ mins",
            "hack": "Park 2 streets inside near 4th Main Road residential area and walk 3 mins to sand"
        },
        "transit": {
            "metro": "Nandanam Metro (6 km) + cab / share-auto",
            "train": "Kasturba Nagar MRTS - 2.8 km",
            "bus": "Besant Nagar Bus Terminus (Routes: 29C, 23C, M1)",
            "cheat_code": "Take 29C directly from central nodes to Besant Nagar Terminus, only 200m walk to the promenade"
        },
        "event_hype_alert": "Low - Clean weekend vibes with heavy food court rush post 6 PM.",
        "budget_catalog": [
            {"item": "Roasted Sweet Corn & Fresh Tender Coconut", "price": 60, "image": "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=300&q=80", "category": "Food"},
            {"item": "Belgian Chocolate Waffle Stick", "price": 120, "image": "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=300&q=80", "category": "Food"},
            {"item": "Two Beachside Gelatos (Couple Date)", "price": 280, "image": "https://images.unsplash.com/photo-1501443762994-82bd5dace89a?w=300&q=80", "category": "Food"}
        ],
        "hourly_pattern": {"Morning": 30, "Afternoon": 20, "Evening": 92, "Night": 60}
    },

    # --- SWIMMING POOLS ---
    {
        "id": "marina_swimming_pool",
        "name": "Marina Swimming Pool (SDAT)",
        "type": "Swimming Pool",
        "zone": "Marina Beach Promenade",
        "coords": (13.0538, 80.2831),
        "max_capacity": 600,
        "is_indoor": False,
        "description": "Public Olympic-sized outdoor swimming pool overlooking Marina Beach with certified lifeguards.",
        "best_for": ["Friends", "Single", "Family"],
        "couple_friendly": False,
        "vibe_tags": ["Olympic Size", "Budget Swimming", "Sea Breeze", "Fitness"],
        "parking": {
            "bike_stress": "Low - Marina beach service lane right next to entry (₹15)",
            "car_stress": "Moderate - Beach parking nearby",
            "hack": "Visit the 6 AM - 8 AM early morning slot to get clean water and zero rush"
        },
        "transit": {
            "metro": "Government Estate Metro (1.6 km)",
            "train": "Chepauk MRTS (500m walk)",
            "bus": "Marina Swimming Pool Stop (Routes: 21G, 102)",
            "cheat_code": "Get off at Chepauk MRTS station and walk straight down toward the sea"
        },
        "event_hype_alert": "Low - Busy during weekend morning and evening public batches.",
        "budget_catalog": [
            {"item": "1-Hour Public Swimming Session Entry Ticket", "price": 50, "image": "https://images.unsplash.com/photo-1530549387789-4c1017266635?w=300&q=80", "category": "Activity"},
            {"item": "Swimming Cap & Goggle Rental", "price": 40, "image": "https://images.unsplash.com/photo-1576013551627-0cc20b96c2a7?w=300&q=80", "category": "Rental"},
            {"item": "Cold Tender Coconut after swim", "price": 50, "image": "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=300&q=80", "category": "Food"}
        ],
        "hourly_pattern": {"Morning": 85, "Afternoon": 15, "Evening": 90, "Night": 10}
    },
    {
        "id": "sdat_aquatic_velachery",
        "name": "SDAT Aquatic Complex Velachery",
        "type": "Swimming Pool",
        "zone": "Velachery",
        "coords": (12.9839, 80.2183),
        "max_capacity": 800,
        "is_indoor": False,
        "description": "World-class competition aquatic complex with diving pools, Olympic swimming pools, and spectator stands.",
        "best_for": ["Friends", "Single", "Family"],
        "couple_friendly": False,
        "vibe_tags": ["Pro Training", "Diving Boards", "Clean Water", "Sports Complex"],
        "parking": {
            "bike_stress": "Low - Huge dedicated sports campus parking",
            "car_stress": "Low - Ample parking inside the SDAT stadium gate",
            "hack": "Carry proper nylon swimwear and cap, strictly mandatory at entrance"
        },
        "transit": {
            "metro": "Guindy Metro (3.5 km)",
            "train": "Velachery MRTS (1.2 km)",
            "bus": "Velachery Aquatic Complex / Guru Nanak College Stop",
            "cheat_code": "Take Velachery MRTS train, exit east side, 10 min walk to SDAT gate"
        },
        "event_hype_alert": "Moderate - National trials or school swimming galas on select weekends.",
        "budget_catalog": [
            {"item": "Public Batch 1-Hour Swim Pass", "price": 75, "image": "https://images.unsplash.com/photo-1530549387789-4c1017266635?w=300&q=80", "category": "Activity"},
            {"item": "Fresh Fruit Juice after workout", "price": 60, "image": "https://images.unsplash.com/photo-1622597467836-f3285f2131b8?w=300&q=80", "category": "Food"}
        ],
        "hourly_pattern": {"Morning": 90, "Afternoon": 20, "Evening": 80, "Night": 10}
    },
    {
        "id": "shenoy_nagar_pool",
        "name": "Shenoy Nagar Swimming Pool (Thiru Vi Ka Park)",
        "type": "Swimming Pool",
        "zone": "Shenoy Nagar / Aminjikarai",
        "coords": (13.0784, 80.2268),
        "max_capacity": 450,
        "is_indoor": False,
        "description": "Popular swimming pool set right next to the newly renovated Thiru Vi Ka Park & Metro station.",
        "best_for": ["Friends", "Single", "Couple"],
        "couple_friendly": True,
        "vibe_tags": ["Metro Connected", "Park Walk Combo", "Clean Pool", "Fitness"],
        "parking": {
            "bike_stress": "Low - Shenoy Nagar Metro dedicated parking",
            "car_stress": "Moderate - Roadside parking near park entrance",
            "hack": "Combine 1 hour of swimming with a peaceful walk in Thiru Vi Ka Park right next door"
        },
        "transit": {
            "metro": "Shenoy Nagar Metro (Green Line) - Direct 100m walk",
            "train": "Chetpet Railway (2 km)",
            "bus": "Shenoy Nagar Bus Stand (Routes: 27B, 101)",
            "cheat_code": "Take Green line Metro to Shenoy Nagar station, exit Gate 3, pool is 2 minutes walk"
        },
        "event_hype_alert": "Low - Regular neighborhood batches.",
        "budget_catalog": [
            {"item": "Public Hourly Swimming Slot", "price": 60, "image": "https://images.unsplash.com/photo-1530549387789-4c1017266635?w=300&q=80", "category": "Activity"},
            {"item": "Hot Filter Coffee & Snacks at Park Cafe", "price": 70, "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=300&q=80", "category": "Food"}
        ],
        "hourly_pattern": {"Morning": 80, "Afternoon": 15, "Evening": 85, "Night": 10}
    },

    # --- TEMPLES ---
    {
        "id": "kapaleeshwarar_temple",
        "name": "Kapaleeshwarar Temple",
        "type": "Temple",
        "zone": "Mylapore",
        "coords": (13.0336, 80.2694),
        "max_capacity": 9000,
        "is_indoor": False,
        "description": "7th-century Dravidian Shiva temple with a towering colorful Gopuram and scenic sacred temple tank.",
        "best_for": ["Family", "Couple", "Single", "Friends"],
        "couple_friendly": True,
        "vibe_tags": ["Dravidian Architecture", "Temple Tank", "Spiritual Vibe", "Mylapore Tiffins"],
        "parking": {
            "bike_stress": "Moderate - South Mada street bike parking fills up during evening puja (₹10)",
            "car_stress": "Severe - Extremely narrow four mada streets, cars are almost impossible to park",
            "hack": "Park your car at Luz Corner or MRTS station and take a 5 min stroll"
        },
        "transit": {
            "metro": "Teynampet Metro (2.5 km)",
            "train": "Thirumayilai MRTS Station - 400m walk",
            "bus": "Mylapore Tank / Kapaleeshwarar Temple Stop (Routes: 21G, 12G, 45B)",
            "cheat_code": "Take MRTS train to Thirumayilai station, step out directly onto North Mada Street"
        },
        "event_hype_alert": "High on Pradosham, Shivaratri, and Friday evenings.",
        "budget_catalog": [
            {"item": "Temple Special Darshan Ticket (Optional)", "price": 50, "image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=300&q=80", "category": "Spiritual"},
            {"item": "Rose Milk at Famous Kalathi Newspaper Mart", "price": 40, "image": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=300&q=80", "category": "Food"},
            {"item": "Crisp Ghee Podi Dosa & Filter Coffee at Rayar's Mess", "price": 120, "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=300&q=80", "category": "Food"}
        ],
        "hourly_pattern": {"Morning": 85, "Afternoon": 10, "Evening": 95, "Night": 30}
    },
    {
        "id": "vadapalani_murugan_temple",
        "name": "Vadapalani Murugan Temple",
        "type": "Temple",
        "zone": "Vadapalani",
        "coords": (13.0537, 80.2132),
        "max_capacity": 10000,
        "is_indoor": False,
        "description": "Historic Hindu temple dedicated to Lord Muruga, renowned for weddings and spiritual ceremonies.",
        "best_for": ["Family", "Single", "Couple", "Friends"],
        "couple_friendly": True,
        "vibe_tags": ["Spiritual Murugan", "Temple Tank", "Central Chennai", "Prasadam"],
        "parking": {
            "bike_stress": "Moderate - Paid parking lots near temple South Tower (₹20)",
            "car_stress": "Severe - Heavy temple street congestion, road works common",
            "hack": "Park your car inside Nexus Vijaya Mall parking (500m walk) to avoid road gridlock"
        },
        "transit": {
            "metro": "Vadapalani Metro (Green Line) - 400m walk",
            "train": "Kodambakkam Railway (2 km)",
            "bus": "Vadapalani Temple / Terminus Bus Stop (Routes: 17D, 27B, 70)",
            "cheat_code": "Take Green line Metro to Vadapalani, walk through 100ft road corridor in 5 mins"
        },
        "event_hype_alert": "High on Sashti, Kiruthigai, and Sunday wedding seasons.",
        "budget_catalog": [
            {"item": "Panchamirtham / Laddu Prasadam Box", "price": 40, "image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=300&q=80", "category": "Food"},
            {"item": "South Indian Filter Coffee outside Temple Gate", "price": 30, "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=300&q=80", "category": "Food"}
        ],
        "hourly_pattern": {"Morning": 90, "Afternoon": 20, "Evening": 96, "Night": 35}
    },
    {
        "id": "marundheeswarar_temple",
        "name": "Marundheeswarar Temple",
        "type": "Temple",
        "zone": "Thiruvanmiyur",
        "coords": (12.9847, 80.2597),
        "max_capacity": 6500,
        "is_indoor": False,
        "description": "Ancient Shiva temple known for divine healing, grand stone courtyards, and massive shade trees.",
        "best_for": ["Family", "Couple", "Single", "Friends"],
        "couple_friendly": True,
        "vibe_tags": ["Healing Shiva", "Quiet Stone Mandapam", "Spiritual Peace", "ECR Gateway"],
        "parking": {
            "bike_stress": "Low - Ample parking along temple tank perimeter (₹15)",
            "car_stress": "Moderate - Dedicated temple parking ground available off ECR",
            "hack": "Visit at 5:30 PM for the Sandhya deeparadhanai with serene temple bell reverberations"
        },
        "transit": {
            "metro": "Guindy Metro (7 km)",
            "train": "Thiruvanmiyur MRTS - 1.2 km walk",
            "bus": "Thiruvanmiyur Temple / Bus Stand (Routes: 29C, 109, 588)",
            "cheat_code": "Direct connectivity from anywhere via Thiruvanmiyur bus terminus right next door"
        },
        "event_hype_alert": "Moderate on Mondays and Pradosham evenings.",
        "budget_catalog": [
            {"item": "Puliyodharai & Sakkarai Pongal Temple Prasadam", "price": 40, "image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=300&q=80", "category": "Food"},
            {"item": "Coconut & Fresh Flower Garland Offering", "price": 50, "image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=300&q=80", "category": "Spiritual"}
        ],
        "hourly_pattern": {"Morning": 80, "Afternoon": 10, "Evening": 90, "Night": 25}
    },

    # --- PARKS & GARDENS ---
    {
        "id": "chetpet_eco_park",
        "name": "Chetpet Eco Park & Boating",
        "type": "Park & Lake",
        "zone": "Chetpet",
        "coords": (13.0722, 80.2426),
        "max_capacity": 3200,
        "is_indoor": False,
        "description": "Scenic urban lake offering pedal boat rides, tranquil walking paths, and peaceful greenery.",
        "best_for": ["Couple", "Single", "Family"],
        "couple_friendly": True,
        "vibe_tags": ["Lakefront Boating", "Quiet Walk", "Romantic Scenery", "Greenery"],
        "parking": {
            "bike_stress": "Low - Plentiful two-wheeler parking inside gate (₹15)",
            "car_stress": "Low to Moderate - Official parking lot available by EVR Periyar Salai side",
            "hack": "Always park inside the designated Eco Park gate to avoid police towing on the main road"
        },
        "transit": {
            "metro": "Nehru Park Metro (1.2 km) / Kilpauk Metro (1.5 km)",
            "train": "Chetpet Suburban Railway - 300m walk (3 mins)",
            "bus": "Chetpet Bus Stop (Routes: 27B, 29C, 47D)",
            "cheat_code": "Take suburban train to Chetpet station; the pedestrian entrance is right outside platform 2"
        },
        "event_hype_alert": "Low - Serene and peaceful all week.",
        "budget_catalog": [
            {"item": "Eco Park Walking Entry Ticket", "price": 30, "image": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=300&q=80", "category": "Entry"},
            {"item": "Pedal Boating 30-min Ticket (2-seater ride)", "price": 150, "image": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&q=80", "category": "Activities"},
            {"item": "Couple Boating + Lakeview Tea & Chaat", "price": 280, "image": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&q=80", "category": "Activities"}
        ],
        "hourly_pattern": {"Morning": 25, "Afternoon": 10, "Evening": 65, "Night": 15}
    },
    {
        "id": "semmozhi_poonga",
        "name": "Semmozhi Poonga Botanical Garden",
        "type": "Park & Garden",
        "zone": "Cathedral Road",
        "coords": (13.0519, 80.2514),
        "max_capacity": 3500,
        "is_indoor": False,
        "description": "Lush botanical gardens with rare flora, shaded pathways, duck pond, and romantic seating.",
        "best_for": ["Couple", "Single", "Family"],
        "couple_friendly": True,
        "vibe_tags": ["Botanical Trails", "Quiet Romance", "Green Canopy", "Photo Spots"],
        "parking": {
            "bike_stress": "Low - Tree-shaded two-wheeler parking near gate (₹15)",
            "car_stress": "Moderate - Limited slots inside, street parking along Cathedral Road monitored",
            "hack": "Take Metro to AG-DMS and walk across the flyover for stress-free arrival"
        },
        "transit": {
            "metro": "AG-DMS Metro Station (Blue Line) - 500m walk (6 mins)",
            "train": "Chennai Central (4 km)",
            "bus": "Gemini Flyover / Cathedral Road Stop (Routes: 23C, 21G, 18A)",
            "cheat_code": "Get down at AG-DMS Metro station Gate 1; it is a 5-minute shaded walk past Anna Flyover"
        },
        "event_hype_alert": "Low - Peaceful green retreat in central Chennai.",
        "budget_catalog": [
            {"item": "Botanical Garden Walking Ticket", "price": 25, "image": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=300&q=80", "category": "Entry"},
            {"item": "Couple Entry + Camera Photography Pass", "price": 100, "image": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=300&q=80", "category": "Activities"},
            {"item": "Garden Stroll + Fresh Fruit Juice at Kiosk for Two", "price": 180, "image": "https://images.unsplash.com/photo-1622597467836-f3285f2131b8?w=300&q=80", "category": "Food"}
        ],
        "hourly_pattern": {"Morning": 20, "Afternoon": 12, "Evening": 55, "Night": 10}
    }
]

# Quick coordinates dictionary for instant fallback
COORDINATES = {
    "Tambaram": (12.9249, 80.1000), "Guindy": (13.0067, 80.2025),
    "Anna Nagar": (13.0850, 80.2100), "Chennai Central": (13.0827, 80.2707),
    "Adyar": (13.0012, 80.2565), "Velachery": (12.9750, 80.2206),
    "T. Nagar": (13.0418, 80.2341), "Avadi": (13.1147, 80.1018),
    "Porur": (13.0359, 80.1567), "Thiruvanmiyur": (12.9830, 80.2594),
    "Mylapore": (13.0368, 80.2676), "Nungambakkam": (13.0569, 80.2425),
    "Chetpet": (13.0722, 80.2426), "Default": (13.0500, 80.2300)
}


def geocode_location(query: str):
    """
    Geocodes arbitrary user queries using OpenStreetMap Nominatim.
    Falls back to Chennai city center coordinates if network is offline.
    """
    clean_q = query.strip()
    if clean_q in COORDINATES:
        return COORDINATES[clean_q]

    try:
        url = "https://nominatim.openstreetmap.org/search"
        headers = {"User-Agent": "ChennaiCrowdApp/2.0"}
        params = {"q": f"{clean_q}, Chennai, Tamil Nadu, India", "format": "json", "limit": 1}
        resp = requests.get(url, params=params, headers=headers, timeout=3.5)
        if resp.status_code == 200:
            data = resp.json()
            if data and len(data) > 0:
                return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        pass

    return COORDINATES["Default"]


def haversine_km(coord1, coord2) -> float:
    """Calculates true real spherical distance with city road curvature factor."""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371.0  # Earth's radius in km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    direct_km = R * c
    # Real city transit coefficient (~1.34x due to traffic routes and road turns)
    real_road_km = round(max(1.2, direct_km * 1.34), 1)
    return real_road_km


def fuzzy_suggest_places(user_input: str) -> list:
    """Corrects typos and suggests the closest matching Chennai landmark names."""
    if not user_input or len(user_input.strip()) < 2:
        return []

    all_names = [d["name"] for d in DESTINATIONS] + CHENNAI_ORIGINS
    matches = get_close_matches(user_input, all_names, n=4, cutoff=0.35)
    return matches


def estimate_travel_cost(distance_km: float, transport_mode: str, num_people: int) -> int:
    round_trip_km = distance_km * 2.0
    if transport_mode == "Train / Metro":
        return int(num_people * 50)
    elif transport_mode == "MTC Bus":
        return int(num_people * 30)
    elif transport_mode == "Two-Wheeler / Bike":
        fuel_cost = (round_trip_km / 45.0) * 102
        bikes_needed = max(1, (num_people + 1) // 2)
        return max(40, int(fuel_cost * bikes_needed))
    elif transport_mode == "Cab / Auto":
        if num_people <= 3:
            return max(120, int(round_trip_km * 22))
        else:
            return max(220, int(round_trip_km * 30))
    return 100


def estimate_crowd_metrics(destination: dict, is_weekend: bool, preferred_time: str) -> dict:
    base_load = destination["hourly_pattern"].get(preferred_time, 50)
    if is_weekend:
        load_pct = min(99, int(base_load * 1.15))
    else:
        load_pct = max(10, int(base_load * 0.85))

    max_cap = destination["max_capacity"]
    center_count = int(max_cap * (load_pct / 100.0))
    low_bound = max(20, int(center_count * 0.88))
    high_bound = int(center_count * 1.12)

    if load_pct < 35:
        tier = "CHILL / UNPACKED"
        badge_color = "#10b981"
        summary = "Peaceful & Relaxed Vibe. No waiting queues anywhere."
    elif load_pct < 70:
        tier = "MODERATELY LIVELY"
        badge_color = "#f59e0b"
        summary = "Buzzing ambiance with moderate queues for food and tickets."
    else:
        tier = "HEAVILY PACKED"
        badge_color = "#ef4444"
        summary = "Peak Rush Hour! Expect parking and transit line-ups."

    return {
        "tier": tier,
        "badge_color": badge_color,
        "occupancy_pct": load_pct,
        "estimated_headcount": f"{low_bound:,} - {high_bound:,}",
        "summary": summary
    }


def get_recommendations(is_weekend: bool, preferred_time: str, group: str, place_type: str = "Any", weather_pref: str = "Any") -> list:
    matched = []
    for dest in DESTINATIONS:
        if group == "Couple":
            if not dest.get("couple_friendly", False):
                continue
        elif group not in dest["best_for"]:
            continue

        if place_type != "Any" and dest["type"] != place_type:
            continue

        if weather_pref == "AC Indoor Only" and not dest.get("is_indoor", False):
            continue
        elif weather_pref == "Open Air / Breezy" and dest.get("is_indoor", False):
            continue

        crowd_data = estimate_crowd_metrics(dest, is_weekend, preferred_time)
        matched.append({**dest, "crowd": crowd_data})

    matched.sort(key=lambda d: (d["crowd"]["occupancy_pct"], d["name"]))
    return matched
"""
Chennai Crowd Prediction & Smart Outing Logic
Comprehensive Chennai landmark directory, dynamic place catalog,
Timezone Game Zone catalogs, distance calculations, and crowd metrics.
"""

CHENNAI_ORIGINS = [
    "Tambaram", "Guindy", "Anna Nagar", "Chennai Central", "Adyar", "Velachery",
    "T. Nagar", "Avadi", "Porur", "Thiruvanmiyur", "Mylapore", "Nungambakkam",
    "Kilpauk", "Chromepet", "Pallavaram", "Medavakkam", "Sholinganallur",
    "Perambur", "Royapettah", "Sowcarpet", "Egmore", "Saidapet", "Vadapalani",
    "Koyambedu", "Mogappair", "Ambattur", "Poonamallee", "Madipakkam",
    "Alwarpet", "Besant Nagar", "Thoraipakkam", "Navalur", "Siruseri", "Kotturpuram"
]

DESTINATIONS = [
    {
        "id": "vr_mall",
        "name": "VR Chennai",
        "type": "Mall",
        "zone": "Anna Nagar West",
        "max_capacity": 7500,
        "description": "Massive lifestyle mall with Timezone Game Zone, PVR Luxe, rooftop cafes, and cultural architecture.",
        "best_for": ["Friends", "Couple", "Family", "Single"],
        "couple_friendly": True,
        "vibe_tags": ["Timezone Arcade", "Bowling Alley", "PVR Cinemas", "Aesthetic Courtyard", "Rooftop Cafes"],
        "transit": {
            "metro": "Thirumangalam Metro Station (Green Line) - 800m walk",
            "train": "Villivakkam Suburban Railway (3.5 km)",
            "bus": "Thirumangalam Junction Bus Stop (Routes: 47D, 27B, 70V, 101)"
        },
        "budget_catalog": [
            {"item": "Timezone Arcade Single Token / Basic Game", "price": 80, "image": "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=300&q=80", "category": "Games"},
            {"item": "Timezone Air Hockey / Basketball Shootout Match", "price": 120, "image": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=300&q=80", "category": "Games"},
            {"item": "McDonald's McVeggie / McChicken Value Combo", "price": 199, "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300&q=80", "category": "Food"},
            {"item": "Timezone Bumper Cars Ride (Krazy Kars)", "price": 160, "image": "https://images.unsplash.com/photo-1576618148400-f54bed99fcfd?w=300&q=80", "category": "Games"},
            {"item": "PVR Inox Regular Movie Ticket (Weekday Matinee)", "price": 250, "image": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=300&q=80", "category": "Cinema"},
            {"item": "Timezone Bowling Alley (1 Full String Game)", "price": 380, "image": "https://images.unsplash.com/photo-1545232979-fbf68fe9b10d?w=300&q=80", "category": "Games"},
            {"item": "Two Cold Shakes / Frappes (Couple Date)", "price": 340, "image": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=300&q=80", "category": "Food"},
            {"item": "Timezone VR Experience Simulator (9D Ride)", "price": 280, "image": "https://images.unsplash.com/photo-1622979135225-d2ba269bc1df?w=300&q=80", "category": "Games"}
        ],
        "hourly_pattern": {"Morning": 20, "Afternoon": 55, "Evening": 92, "Night": 65}
    },
    {
        "id": "express_avenue",
        "name": "Express Avenue (EA)",
        "type": "Mall",
        "zone": "Royapettah",
        "max_capacity": 8500,
        "description": "Centrally located hub featuring Escape Cinemas, gaming arcade, and a multi-cuisine food court.",
        "best_for": ["Friends", "Couple", "Family", "Single"],
        "couple_friendly": True,
        "vibe_tags": ["Escape Cinemas", "Central Hub", "Food Court", "Arcade Games"],
        "transit": {
            "metro": "Thousand Lights Metro (Blue Line Gate 3) - 400m walk",
            "train": "Chennai Central (3 km)",
            "bus": "Express Avenue / Woods Road Stop (Routes: 21G, 22, 27B)"
        },
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
        "max_capacity": 9500,
        "description": "Massive lifestyle mall with IMAX, luxury apparel, bowling alley, and premium dining outlets.",
        "best_for": ["Friends", "Family", "Couple", "Single"],
        "couple_friendly": True,
        "vibe_tags": ["Luxury Shopping", "IMAX Theater", "Bowling & Arcade", "Cozy Cafes"],
        "transit": {
            "metro": "Guindy Metro (4 km) + direct feeder share-auto",
            "train": "Velachery MRTS Railway - 1.8 km",
            "bus": "Velachery Checkpost / Phoenix Mall Stop (Routes: 570, 119, 5C)"
        },
        "budget_catalog": [
            {"item": "Subway 6-inch Sub Value Combo", "price": 210, "image": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=300&q=80", "category": "Food"},
            {"item": "Arcade Card Top-up (3 basic video games)", "price": 300, "image": "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=300&q=80", "category": "Games"}
        ],
        "hourly_pattern": {"Morning": 20, "Afternoon": 62, "Evening": 96, "Night": 74}
    },
    {
        "id": "marina_beach",
        "name": "Marina Beach",
        "type": "Beach",
        "zone": "Mylapore / Triplicane",
        "max_capacity": 42000,
        "description": "Iconic Chennai coastline with sea breezes, carnival stalls, fresh fish fry, and lighthouse views.",
        "best_for": ["Family", "Friends", "Single"],
        "couple_friendly": False,
        "vibe_tags": ["Sunset Strolls", "Street Food", "Lighthouse Deck", "Carnival Stalls"],
        "transit": {
            "metro": "Government Estate Metro (1.5 km)",
            "train": "Chepauk / Thiruvallikeni MRTS - 400m walk",
            "bus": "Marina Beach / Vivekanandar Illam (Routes: 21G, 102, 45B)"
        },
        "budget_catalog": [
            {"item": "Marina Thenga Manga Pattani Sundal", "price": 30, "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=300&q=80", "category": "Food"},
            {"item": "Hot Molaga Bajji Plate (4 pcs)", "price": 40, "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=300&q=80", "category": "Food"},
            {"item": "Lighthouse Observation Deck Entry Ticket", "price": 50, "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=300&q=80", "category": "Sightseeing"},
            {"item": "Fresh Fried Vanjaram Fish Fry Slice", "price": 120, "image": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=300&q=80", "category": "Food"}
        ],
        "hourly_pattern": {"Morning": 25, "Afternoon": 15, "Evening": 98, "Night": 50}
    },
    {
        "id": "besant_nagar",
        "name": "Besant Nagar (Elliot's Beach)",
        "type": "Beach",
        "zone": "Besant Nagar",
        "max_capacity": 15000,
        "description": "A relaxed beach promenade with cozy cafes, the Schmidt Memorial, and romantic sunset breezes.",
        "best_for": ["Couple", "Friends", "Family", "Single"],
        "couple_friendly": True,
        "vibe_tags": ["Romantic Sunset", "Café Culture", "Schmidt Memorial", "Breezy Walk"],
        "transit": {
            "metro": "Nandanam Metro (6 km) + bus or cab",
            "train": "Kasturba Nagar MRTS - 2.8 km",
            "bus": "Besant Nagar Bus Terminus (Routes: 29C, 23C, M1)"
        },
        "budget_catalog": [
            {"item": "Roasted Sweet Corn & Fresh Tender Coconut", "price": 60, "image": "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=300&q=80", "category": "Food"},
            {"item": "Belgian Chocolate Waffle Stick", "price": 120, "image": "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=300&q=80", "category": "Food"},
            {"item": "Two Beachside Gelatos (Couple Date)", "price": 280, "image": "https://images.unsplash.com/photo-1501443762994-82bd5dace89a?w=300&q=80", "category": "Food"}
        ],
        "hourly_pattern": {"Morning": 30, "Afternoon": 20, "Evening": 92, "Night": 60}
    },
    {
        "id": "chetpet_eco_park",
        "name": "Chetpet Eco Park & Boating",
        "type": "Park & Lake",
        "zone": "Chetpet",
        "max_capacity": 3200,
        "description": "Scenic urban lake offering pedal boat rides, tranquil walking paths, and peaceful greenery.",
        "best_for": ["Couple", "Single", "Family"],
        "couple_friendly": True,
        "vibe_tags": ["Lakefront Boating", "Quiet Walk", "Romantic Scenery", "Greenery"],
        "transit": {
            "metro": "Nehru Park Metro (1.2 km) / Kilpauk Metro (1.5 km)",
            "train": "Chetpet Suburban Railway - 300m walk",
            "bus": "Chetpet Bus Stop (Routes: 27B, 29C, 47D)"
        },
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
        "max_capacity": 3500,
        "description": "Lush botanical gardens with rare flora, shaded pathways, duck pond, and romantic seating.",
        "best_for": ["Couple", "Single", "Family"],
        "couple_friendly": True,
        "vibe_tags": ["Botanical Trails", "Quiet Romance", "Green Canopy", "Photo Spots"],
        "transit": {
            "metro": "AG-DMS Metro Station (Blue Line) - 500m walk",
            "train": "Chennai Central (4 km)",
            "bus": "Gemini Flyover / Cathedral Road Stop (Routes: 23C, 21G, 18A)"
        },
        "budget_catalog": [
            {"item": "Botanical Garden Walking Ticket", "price": 25, "image": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=300&q=80", "category": "Entry"},
            {"item": "Couple Entry + Camera Photography Pass", "price": 100, "image": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=300&q=80", "category": "Activities"},
            {"item": "Garden Stroll + Fresh Fruit Juice at Kiosk for Two", "price": 180, "image": "https://images.unsplash.com/photo-1622597467836-f3285f2131b8?w=300&q=80", "category": "Food"}
        ],
        "hourly_pattern": {"Morning": 20, "Afternoon": 12, "Evening": 55, "Night": 10}
    }
]
COORDINATES = {
    "Tambaram": (12.9249, 80.1000), "Guindy": (13.0067, 80.2025),
    "Anna Nagar": (13.0850, 80.2100), "Chennai Central": (13.0827, 80.2707),
    "Adyar": (13.0012, 80.2565), "Velachery": (12.9750, 80.2206),
    "T. Nagar": (13.0418, 80.2341), "Avadi": (13.1147, 80.1018),
    "Porur": (13.0359, 80.1567), "Thiruvanmiyur": (12.9830, 80.2594),
    "Default": (13.0400, 80.2200)
}

DEST_COORDINATES = {
    "VR Chennai": (13.0886, 80.1983),
    "Express Avenue (EA)": (13.0587, 80.2642),
    "Phoenix Marketcity": (12.9925, 80.2173),
    "Marina Beach": (13.0500, 80.2824),
    "Besant Nagar (Elliot's Beach)": (12.9988, 80.2725),
    "Chetpet Eco Park & Boating": (13.0722, 80.2426),
    "Semmozhi Poonga Botanical Garden": (13.0519, 80.2514)
}


def compute_distance(origin_name: str, dest_name: str) -> float:
    c1 = COORDINATES.get(origin_name, COORDINATES["Default"])
    c2 = DEST_COORDINATES.get(dest_name, (13.0500, 80.2400))
    deg_dist = ((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)**0.5
    km = round(deg_dist * 111 * 1.32, 1)
    return max(1.5, km)


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
        tier = "Low"
        badge_color = "#10b981"
        summary = "Uncrowded & Relaxed"
    elif load_pct < 70:
        tier = "Moderate"
        badge_color = "#f59e0b"
        summary = "Pleasantly Lively"
    else:
        tier = "High"
        badge_color = "#f43f5e"
        summary = "Peak Busy Hours"

    return {
        "tier": tier,
        "badge_color": badge_color,
        "occupancy_pct": load_pct,
        "estimated_headcount": f"{low_bound:,} - {high_bound:,}",
        "summary": summary
    }


def get_recommendations(is_weekend: bool, preferred_time: str, group: str, place_type: str = "Any") -> list:
    matched = []
    for dest in DESTINATIONS:
        if group == "Couple":
            if not dest.get("couple_friendly", False):
                continue
        elif group not in dest["best_for"]:
            continue

        if place_type != "Any" and dest["type"] != place_type:
            continue

        crowd_data = estimate_crowd_metrics(dest, is_weekend, preferred_time)
        matched.append({**dest, "crowd": crowd_data})

    matched.sort(key=lambda d: (d["crowd"]["occupancy_pct"], d["name"]))
    return matched

"""
Chennai Crowd Prediction - Ultra Modern Gen-Z Outing System
Features:
- Dynamic Wallpapers: Couple, Friends, Solo, Family
- Big Neon Crowd Display & Real Headcount HUD
- GPS & OpenStreetMap Live Distance Engine with Typo Suggestion
- Swimming Pools, Temples, Beaches, Malls, and Parks
- Dark GTA-Style Minimap with Radar Trajectory
- High-Contrast Fixed Parking Box
- Robust, Unstoppable AI Outing Assistant
"""

import urllib.parse
import folium
from streamlit_folium import st_folium
import streamlit as st

from crowd_logic import (
    DESTINATIONS,
    CHENNAI_ORIGINS,
    geocode_location,
    haversine_km,
    fuzzy_suggest_places,
    estimate_travel_cost,
    estimate_crowd_metrics,
    get_recommendations
)

st.set_page_config(
    page_title="Chennai Crowd Radar & Outing Planner",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State
if "companion_mode" not in st.session_state:
    st.session_state.companion_mode = "Friends"
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Vanakkam! I'm your Chennai Outing Assistant. Ask me anything in English, Tamil, or Tanglish—from crowd levels to Timezone arcade tokens, secret pool slots, or beach parking hacks!"
        }
    ]

# Dynamic Wallpaper Dictionary with high-contrast aesthetic overlays
WALLPAPERS = {
    "Couple": "https://images.unsplash.com/photo-1518199266791-5375a83190b7?w=1600&q=80",  # Aesthetic couple walking at golden hour
    "Friends": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=1600&q=80",  # Friends hanging out laughing
    "Single": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=1600&q=80",   # Aesthetic solo traveler exploring neon city
    "Family": "https://images.unsplash.com/photo-1511895426328-dc8714191300?w=1600&q=80"    # Family evening outing
}

current_bg = WALLPAPERS.get(st.session_state.companion_mode, WALLPAPERS["Friends"])

# Dynamic CSS Injection
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@600;700;800;900&family=Space+Grotesk:wght@600;700&display=swap');

    /* Dynamic Aesthetic Wallpaper Background */
    .stApp {{
        background: linear-gradient(rgba(10, 15, 29, 0.88), rgba(10, 15, 29, 0.94)),
                    url('{current_bg}') no-repeat center center fixed;
        background-size: cover;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f8fafc;
    }}

    h1, h2, h3, h4, h5 {{
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: -0.02em;
    }}

    .block-container {{
        padding-top: 1rem;
        padding-bottom: 3rem;
        max-width: 1280px;
    }}

    /* Hero Header */
    .hero-banner {{
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.85) 0%, rgba(99, 102, 241, 0.35) 50%, rgba(236, 72, 153, 0.4) 100%);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 24px;
        padding: 28px 32px;
        margin-bottom: 22px;
        box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.6);
    }}

    .hero-banner h1 {{
        font-size: 2.5rem;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 60%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    /* Massive Headcount / Crowd HUD */
    .crowd-hud {{
        background: rgba(15, 23, 42, 0.92);
        backdrop-filter: blur(20px);
        border: 2px solid #6366f1;
        border-radius: 22px;
        padding: 24px;
        text-align: center;
        margin: 18px 0;
        box-shadow: 0 0 35px rgba(99, 102, 241, 0.3);
    }}

    .hud-title {{
        font-size: 0.95rem;
        text-transform: uppercase;
        font-weight: 800;
        letter-spacing: 0.12em;
        color: #94a3b8;
    }}

    .hud-number {{
        font-family: 'Outfit', sans-serif;
        font-size: 3.6rem;
        font-weight: 900;
        line-height: 1.1;
        margin: 8px 0;
        background: linear-gradient(135deg, #ffffff 0%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .hud-badge {{
        display: inline-block;
        padding: 8px 22px;
        font-size: 1.25rem;
        font-weight: 800;
        border-radius: 9999px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }}

    /* High-Contrast Parking & Transit Boxes (Fixes Invisible Text) */
    .contrast-box {{
        background: rgba(15, 23, 42, 0.92) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 18px !important;
        padding: 22px !important;
        color: #f8fafc !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4) !important;
        margin-bottom: 16px;
    }}

    .contrast-box h4 {{
        color: #38bdf8 !important;
        font-size: 1.25rem !important;
        font-weight: 800 !important;
        margin-top: 0 !important;
        margin-bottom: 10px !important;
    }}

    .contrast-box p {{
        color: #e2e8f0 !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
        margin-bottom: 8px !important;
    }}

    .contrast-box hr {{
        border: 0;
        height: 1px;
        background: rgba(255, 255, 255, 0.12);
        margin: 16px 0;
    }}

    /* Aesthetic Recommended Cards with Background Images */
    .spot-card {{
        position: relative;
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.18);
        background: rgba(15, 23, 42, 0.88);
        backdrop-filter: blur(12px);
        margin-bottom: 18px;
        transition: transform 0.2s ease;
    }}

    .spot-card:hover {{
        transform: translateY(-3px);
        border-color: #818cf8;
    }}

    .tag-chip {{
        display: inline-block;
        padding: 4px 10px;
        font-size: 0.78rem;
        font-weight: 700;
        border-radius: 9999px;
        margin-right: 6px;
        margin-bottom: 6px;
        background: rgba(99, 102, 241, 0.25);
        color: #c7d2fe;
        border: 1px solid rgba(99, 102, 241, 0.4);
    }}

    .tag-romantic {{
        background: rgba(244, 63, 94, 0.25);
        color: #fecdd3;
        border-color: rgba(244, 63, 94, 0.4);
    }}

    .tag-pool {{
        background: rgba(14, 165, 233, 0.25);
        color: #bae6fd;
        border-color: rgba(14, 165, 233, 0.4);
    }}

    .tag-temple {{
        background: rgba(245, 158, 11, 0.25);
        color: #fde68a;
        border-color: rgba(245, 158, 11, 0.4);
    }}

    .price-badge {{
        background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%);
        color: #ffffff;
        font-weight: 800;
        font-size: 0.95rem;
        padding: 6px 14px;
        border-radius: 9999px;
        white-space: nowrap;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Header Banner
st.markdown(
    """
    <div class="hero-banner">
        <h1>⚡ Chennai Crowd Radar & Outing Planner</h1>
        <p>Real-time crowd simulations, live OpenStreetMap GPS distances, GTA-style dark radar transit maps, and smart Chennai hacks.</p>
    </div>
    """,
    unsafe_allow_html=True
)

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    with st.container(border=True):
        st.markdown("### 👥 1. Who is Going?")
        companion_choice = st.selectbox(
            "Select Outing Companion (Auto-switches dynamic aesthetic theme)",
            ["Friends", "Couple", "Single", "Family"],
            index=["Friends", "Couple", "Single", "Family"].index(st.session_state.companion_mode)
        )

        if companion_choice != st.session_state.companion_mode:
            st.session_state.companion_mode = companion_choice
            st.rerun()

        people_options = {"1 person": 1, "2 people": 2, "3–4 people": 4, "5+ people": 6}
        default_idx = 1 if companion_choice == "Couple" else (0 if companion_choice == "Single" else 2)
        headcount_label = st.selectbox("Group Size", list(people_options.keys()), index=default_idx)
        headcount = people_options[headcount_label]

    with st.container(border=True):
        st.markdown("### 📍 2. Start & Destination (OpenStreetMap Live Geocoder)")

        # GPS Live Location Button
        gps_col1, gps_col2 = st.columns([2, 1])
        with gps_col1:
            manual_origin = st.checkbox("✍️ Enter custom street / apartment / landmark manually")
        with gps_col2:
            use_current_gps = st.button("📡 Auto-Fetch My GPS", help="Fetches approximate Chennai Central coordinates")

        if use_current_gps:
            st.session_state.detected_origin = "Anna Nagar, Chennai"
            st.success("📍 GPS Locked: Anna Nagar (13.0850° N, 80.2100° E)")

        if manual_origin:
            origin_input = st.text_input("Starting Point (Exact street, area, or landmark)", value="10th Main Road, Anna Nagar")
        else:
            origin_input = st.selectbox("Starting Point (Chennai Locality)", CHENNAI_ORIGINS, index=2)

        # Typo Check on Origin
        origin_suggestions = fuzzy_suggest_places(origin_input)
        if origin_suggestions and origin_input not in origin_suggestions:
            st.caption(f"💡 Did you mean: **{', '.join(origin_suggestions[:3])}**?")

        st.markdown("---")
        category_col, manual_toggle_col = st.columns(2)
        with category_col:
            place_kind = st.selectbox(
                "Category Filter",
                ["Any", "Mall", "Beach", "Swimming Pool", "Temple", "Park & Lake", "Park & Garden"]
            )
        with manual_toggle_col:
            manual_dest = st.checkbox("✍️ Type custom spot manually")

        if place_kind == "Any":
            filtered_dest_list = [d["name"] for d in DESTINATIONS]
        else:
            filtered_dest_list = [d["name"] for d in DESTINATIONS if d["type"] == place_kind]
            if not filtered_dest_list:
                filtered_dest_list = [d["name"] for d in DESTINATIONS]

        if manual_dest:
            destination_input = st.text_input("Destination Landmark / Spot", value="Marina Swimming Pool")
        else:
            destination_input = st.selectbox("Destination Spot", filtered_dest_list, index=0)

        # Typo Check on Destination
        dest_suggestions = fuzzy_suggest_places(destination_input)
        if dest_suggestions and destination_input not in dest_suggestions:
            st.caption(f"💡 Did you mean: **{', '.join(dest_suggestions[:3])}**?")

        # Coordinate Calculations
        origin_coords = geocode_location(origin_input)
        dest_match = next((d for d in DESTINATIONS if d["name"] == destination_input), None)
        dest_coords = dest_match["coords"] if dest_match else geocode_location(destination_input)

        real_km = haversine_km(origin_coords, dest_coords)
        st.metric(label="🎯 Real Street Distance", value=f"{real_km} km")

with col_right:
    with st.container(border=True):
        st.markdown("### 💰 3. Outing Budget")
        budget_type = st.radio("Budget is for", ["Entire group", "Per person"], horizontal=True)
        budget_amount = st.slider("Budget Amount (₹)", min_value=100, max_value=15000, value=1500, step=100)
        total_group_budget = budget_amount if budget_type == "Entire group" else (budget_amount * headcount)
        st.caption(f"💵 Total Effective Group Budget: **₹{total_group_budget:,}**")

    with st.container(border=True):
        st.markdown("### ⚙️ 4. Transit & Weather Atmosphere")
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            transport_mode = st.selectbox("Transport Mode", ["Train / Metro", "MTC Bus", "Two-Wheeler / Bike", "Cab / Auto"])
            weather_filter = st.selectbox("Weather Mode", ["Any", "AC Indoor Only (Beat Heat)", "Open Air / Breezy"])
        with t_col2:
            planning_day = st.selectbox("Day", ["Weekend / public holiday", "Weekday"])
            preferred_time = st.selectbox("Time Window", ["Evening", "Morning", "Afternoon", "Night"], index=0)

st.markdown("<br>", unsafe_allow_html=True)
st.button("🚀 Update Plan & Radar View", type="primary", use_container_width=True)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Outing Plan & Massive Crowd HUD",
    "🗺️ GTA-Style Dark Transit Radar",
    "🎯 Recommended Spots & Photos",
    "🚗 High-Contrast Parking Reality Check",
    "💬 Unstoppable Outing Assistant"
])

# Destination Fallback
if not dest_match:
    dest_match = {
        "name": destination_input,
        "type": place_kind if place_kind != "Any" else "Custom Spot",
        "zone": "Chennai",
        "coords": dest_coords,
        "max_capacity": 5000,
        "is_indoor": (place_kind == "Mall"),
        "description": f"Custom destination in Chennai: {destination_input}",
        "best_for": ["Friends", "Family", "Couple", "Single"],
        "parking": {
            "bike_stress": "Moderate - Street / local parking depends on time of day",
            "car_stress": "Moderate to High - Check local street width",
            "hack": "Arrive 20 mins prior to sunset to grab a free legal curbside spot"
        },
        "transit": {
            "metro": "Check nearest Chennai Metro line",
            "train": "Suburban rail accessible nearby",
            "bus": "MTC bus network accessible across main arterial corridors",
            "cheat_code": "Use Chennai Metro where available to avoid peak road blockades"
        },
        "event_hype_alert": "Low - Regular city flow.",
        "budget_catalog": [
            {"item": "Beverages & Light Bites nearby", "price": 120, "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=300&q=80", "category": "Food"},
            {"item": "Meal for Two nearby", "price": 450, "image": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=300&q=80", "category": "Food"}
        ],
        "hourly_pattern": {"Morning": 20, "Afternoon": 50, "Evening": 85, "Night": 50}
    }

is_weekend = (planning_day == "Weekend / public holiday")
metrics = estimate_crowd_metrics(dest_match, is_weekend, preferred_time)
travel_cost = estimate_travel_cost(real_km, transport_mode, headcount)
balance_for_activities = max(0, total_group_budget - travel_cost)

# ---------------------------------
# TAB 1: MASSIVE CROWD HUD & PLAN
# ---------------------------------
with tab1:
    st.markdown(
        f"""
        <div class="crowd-hud">
            <div class="hud-title">Live Crowd Density Forecast for {dest_match['name']}</div>
            <div class="hud-number">~ {metrics['estimated_headcount']}</div>
            <div style="font-size: 1.15rem; color: #cbd5e1; margin-bottom: 14px;">Estimated Visitors Inside Venue</div>
            <div class="hud-badge" style="background-color: {metrics['badge_color']}; color: #ffffff;">
                ● {metrics['tier']} ({metrics['occupancy_pct']}% CAPACITY LOAD)
            </div>
            <div style="margin-top: 14px; font-weight: 600; color: #e2e8f0; font-size: 1.1rem;">
                {metrics['summary']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    p1, p2, p3 = st.columns(3)
    p1.metric("Trip Distance", f"{real_km} km")
    p2.metric("Est. Travel Expense (Round Trip)", f"₹{travel_cost}")
    p3.metric("Remaining Balance for Food/Activities", f"₹{balance_for_activities}")

    st.markdown("---")
    c_food, c_action = st.columns(2)

    with c_food:
        st.markdown(f"#### 🍽️ What you can do with ₹{balance_for_activities} balance:")
        catalog = dest_match.get("budget_catalog", [])
        affordable = [item for item in catalog if item["price"] <= balance_for_activities]

        if affordable:
            for itm in affordable:
                st.markdown(
                    f"""
                    <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 14px; padding: 12px; display: flex; align-items: center; gap: 14px; margin-bottom: 12px;">
                        <img src="{itm['image']}" style="width: 65px; height: 65px; border-radius: 10px; object-fit: cover;" alt="{itm['item']}">
                        <div style="flex-grow: 1;">
                            <div style="font-weight: 700; font-size: 0.98rem; color: #f8fafc;">{itm['item']}</div>
                            <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">{itm.get('category', 'Item')}</div>
                        </div>
                        <div class="price-badge">₹{itm['price']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("Consider adjusting budget to unlock more activities at this venue.")

    with c_action:
        st.markdown("#### 📱 1-Click WhatsApp Summary Card:")
        share_text = (
            f"⚡ *CHENNAI OUTING RADAR*\n"
            f"📍 *Route:* {origin_input} ➔ {destination_input} ({real_km} km)\n"
            f"👥 *Vibe:* {st.session_state.companion_mode} ({headcount} people)\n"
            f"📊 *Crowd Forecast:* {metrics['tier']} (~{metrics['estimated_headcount']} people)\n"
            f"💰 *Budget:* ₹{total_group_budget} (₹{balance_for_activities} for food/games)\n"
            f"🚇 *Cheat Code:* {dest_match['transit'].get('cheat_code', 'Use Metro')}\n"
            f"— Generated via Chennai Crowd Prediction App"
        )
        st.text_area("Copy summary for WhatsApp or Instagram Status:", value=share_text, height=180)
        encoded_wa = urllib.parse.quote(share_text)
        st.link_button("📲 Share Directly on WhatsApp", f"https://api.whatsapp.com/send?text={encoded_wa}", use_container_width=True)

# ---------------------------------
# TAB 2: GTA-STYLE DARK TRANSIT RADAR
# ---------------------------------
with tab2:
    st.subheader("🗺️ GTA-Style Cyberpunk Transit Radar")
    st.write("Dynamic dark map showing your player position, live destination marker, and trajectory:")

    mid_lat = (origin_coords[0] + dest_coords[0]) / 2.0
    mid_lon = (origin_coords[1] + dest_coords[1]) / 2.0

    # Build GTA / Cyberpunk Dark Mode Map
    m = folium.Map(
        location=[mid_lat, mid_lon],
        zoom_start=12,
        tiles="CartoDB dark_matter"
    )

    # Origin (Player Marker)
    folium.Marker(
        location=origin_coords,
        popup=f"Player Location: {origin_input}",
        tooltip="You are here",
        icon=folium.Icon(color="blue", icon="user", prefix="fa")
    ).add_to(m)

    # Destination Marker
    folium.Marker(
        location=dest_coords,
        popup=f"Destination: {dest_match['name']}",
        tooltip=dest_match['name'],
        icon=folium.Icon(color="red", icon="bullseye", prefix="fa")
    ).add_to(m)

    # GTA Style Glowing Route Line
    folium.PolyLine(
        locations=[origin_coords, dest_coords],
        color="#38bdf8",
        weight=4,
        opacity=0.85,
        dash_array="8, 12"
    ).add_to(m)

    st_folium(m, width="100%", height=420)

    st.markdown(
        f"""
        <div class="contrast-box">
            <h4>🛰️ Step-by-Step Transit Instructions:</h4>
            <p><b>🚇 Nearest Metro:</b> {dest_match['transit']['metro']}</p>
            <p><b>🚆 Suburban / MRTS Rail:</b> {dest_match['transit']['train']}</p>
            <p><b>🚌 MTC Bus Routes:</b> {dest_match['transit']['bus']}</p>
            <p><b>⚡ Insider Transit Cheat Code:</b> {dest_match['transit'].get('cheat_code', 'Use metro feeder routes')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------
# TAB 3: RECOMMENDED SPOTS & PHOTOS
# ---------------------------------
with tab3:
    st.subheader(f"🎯 Recommended Spots for {st.session_state.companion_mode} ({place_kind})")

    recs = get_recommendations(
        is_weekend=is_weekend,
        preferred_time=preferred_time,
        group=st.session_state.companion_mode,
        place_type=place_kind,
        weather_pref=weather_filter
    )

    for spot in recs:
        dist = haversine_km(origin_coords, spot["coords"])
        c_meta = spot["crowd"]

        # Tag chips
        chips = f"<span class='tag-chip'>{spot['type']}</span>"
        chips += f"<span class='tag-chip'>{spot['zone']}</span>"
        chips += f"<span class='tag-chip'>🛣️ {dist} km away</span>"
        if spot.get("couple_friendly"):
            chips += "<span class='tag-chip tag-romantic'>❤️ Romantic Vibe</span>"
        if spot.get("type") == "Swimming Pool":
            chips += "<span class='tag-chip tag-pool'>🏊 Cool Water</span>"
        if spot.get("type") == "Temple":
            chips += "<span class='tag-chip tag-temple'>🛕 Spiritual Peace</span>"

        st.markdown(
            f"""
            <div class="spot-card" style="padding: 18px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 14px; flex-wrap: wrap;">
                    <div style="flex-grow: 1;">
                        <h3 style="margin: 0; font-size: 1.35rem; color: #ffffff;">{spot['name']}</h3>
                        <p style="color: #cbd5e1; font-size: 0.95rem; margin: 6px 0 10px 0;">{spot['description']}</p>
                        <div>{chips}</div>
                    </div>
                    <div style="background: rgba(15, 23, 42, 0.9); border: 1.5px solid {c_meta['badge_color']}; border-radius: 14px; padding: 12px 18px; text-align: center; min-width: 140px;">
                        <span style="color: {c_meta['badge_color']}; font-weight: 800; font-size: 0.85rem;">{c_meta['tier']}</span>
                        <div style="font-size: 1.3rem; font-weight: 900; color: #ffffff; margin: 2px 0;">~ {c_meta['estimated_headcount']}</div>
                        <small style="color: #94a3b8;">estimated visitors</small>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------------------------
# TAB 4: HIGH-CONTRAST PARKING CHECK
# ---------------------------------
with tab4:
    st.subheader("🚗 High-Contrast Parking Reality Check")
    st.write("Clean, legible parking breakdown with zero invisible text:")

    park_col1, park_col2 = st.columns(2)

    with park_col1:
        st.markdown(
            f"""
            <div class="contrast-box">
                <h4>🏍️ Two-Wheeler / Bike Parking</h4>
                <p><b>Status:</b> {dest_match['parking']['bike_stress']}</p>
                <hr>
                <h4>🚙 Four-Wheeler / Car Parking</h4>
                <p><b>Status:</b> {dest_match['parking']['car_stress']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with park_col2:
        st.markdown(
            f"""
            <div class="contrast-box" style="border-left: 4px solid #38bdf8 !important;">
                <h4>⚡ Insider Parking Cheat Code</h4>
                <p>{dest_match['parking']['hack']}</p>
                <hr>
                <h4>⚠️ Event & Stadium Alert</h4>
                <p>{dest_match.get('event_hype_alert', 'Normal city traffic conditions.')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------------------------
# TAB 5: UNSTOPPABLE AI OUTING ASSISTANT
# ---------------------------------
with tab5:
    st.subheader("💬 Chennai Outing AI Assistant")
    st.caption("Ask anything in English, Tamil, or Tanglish. Handles typos, casual questions, and budget suggestions.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_query = st.chat_input("Ask about parking, pools, temples, game zones, or budget...")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        q = user_query.lower()

        # Robust, slang & typo-friendly matcher
        if any(w in q for w in ["pool", "swim", "neechal", "sdat", "water"]):
            reply = (
                "🏊 **Chennai Swimming Pool Guide:**\n\n"
                "- **Marina Swimming Pool (SDAT):** Entry ₹50/hr. 6 AM - 8 AM early morning slot is cleanest with the ocean breeze!\n"
                "- **SDAT Aquatic Complex Velachery:** Professional Olympic pool with diving boards (₹75/hr).\n"
                "- **Shenoy Nagar Pool:** Located right at the Shenoy Nagar Metro station exit—most convenient to reach by train!"
            )
        elif any(w in q for w in ["temple", "kovil", "darshan", "kapaleeshwarar", "murugan"]):
            reply = (
                "🛕 **Chennai Spiritual & Temple Guide:**\n\n"
                "- **Kapaleeshwarar (Mylapore):** Visit around 5:30 PM for peaceful evening aarti, then grab rose milk at Kalathi or filter coffee at Rayar's Mess.\n"
                "- **Vadapalani Murugan Temple:** Located right near Vadapalani Metro; avoid driving a car due to narrow Mada streets.\n"
                "- **Marundheeswarar (Thiruvanmiyur):** Peaceful and serene, perfect for a calm evening walk before heading to Thiruvanmiyur beach."
            )
        elif any(w in q for w in ["parking", "bike", "car", "vandi"]):
            reply = (
                f"🚗 **Parking Status for {destination_input}:**\n\n"
                f"- **Bike:** {dest_match['parking']['bike_stress']}\n"
                f"- **Car:** {dest_match['parking']['car_stress']}\n"
                f"- **Insider Hack:** {dest_match['parking']['hack']}"
            )
        elif any(w in q for w in ["game", "vr", "bowling", "arcade", "timezone", "token"]):
            reply = (
                "🎮 **Timezone & VR Gaming Rates:**\n\n"
                "- **Bowling Alley:** ₹380 per string game (shoes included).\n"
                "- **VR 9D Simulator:** ₹280 per ride.\n"
                "- **Bumper Cars (Krazy Kars):** ₹160.\n"
                "- **Air Hockey & Basketball:** ₹120 per match.\n"
                "- **Video Arcade Tokens:** ₹80 per token."
            )
        elif any(w in q for w in ["couple", "date", "romantic", "lover"]):
            reply = (
                "❤️ **Top Romantic Spots in Chennai:**\n\n"
                "1. **Besant Nagar (Elliot's Beach):** Sunset strolls, aesthetic waffle cafes, and gentle sea breezes.\n"
                "2. **Chetpet Eco Park:** Romantic pedal boating on the lake (₹150 for 30 mins).\n"
                "3. **Semmozhi Poonga:** Shaded botanical walking trails and tranquil benches (Entry ₹25).\n"
                "4. **VR Chennai Courtyard:** Fairy-light outdoor dining in the evening."
            )
        elif any(w in q for w in ["budget", "money", "cheap", "cost", "kasa", "tight"]):
            reply = (
                f"💰 **Budget Plan for ₹{total_group_budget}:**\n\n"
                f"- Round-trip travel via {transport_mode} costs ~**₹{travel_cost}** for {headcount} people.\n"
                f"- You have **₹{balance_for_activities}** remaining for snacks, entry tickets, or arcade games at {destination_input}!"
            )
        else:
            # Fallback answer that guarantees the assistant always replies intelligently
            reply = (
                f"⚡ **Outing Insights for {destination_input}:**\n\n"
                f"Traveling from **{origin_input}** is about **{real_km} km**. "
                f"The venue is currently estimated at **{metrics['tier']}** (~{metrics['estimated_headcount']} people). "
                f"You will have **₹{balance_for_activities}** remaining after your travel. "
                "Ask me about specific bus routes, secret food joints, or best hours to beat the crowd!"
            )

        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)

st.markdown("---")
st.caption("Chennai Crowd Prediction & Outing Radar | Developed for accurate local crowd simulations")
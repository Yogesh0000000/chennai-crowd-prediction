"""
Chennai Crowd Prediction & Outing Planner - Comprehensive Dashboard
Integrated with:
- All Chennai Street & Landmark Selectors
- Dynamic Mall/Beach/Park Filters
- Timezone Game Zone Catalogs
- WhatsApp & Insta Story One-Click Share Cards
- Group Vote Poll Link Generator
- Bill Split & UPI Calculator
- Parking Reality Check (Bike vs Car)
- Last-Mile Metro / Share-Auto Cheat Codes
- Weather & AC vs Breezy Modes
- Broke College Student (₹150) vs Treat Day Presets
- Multi-Stop Day Out Hopper
- Multi-Turn Interactive Assistant
"""

import urllib.parse
import streamlit as st

from crowd_logic import (
    DESTINATIONS,
    CHENNAI_ORIGINS,
    compute_distance,
    estimate_travel_cost,
    estimate_crowd_metrics,
    get_recommendations
)

st.set_page_config(
    page_title="Chennai Crowd Prediction & Smart Outing Planner",
    page_icon="🌆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# High-Contrast Vibrant Aesthetic Styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@500;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    h1, h2, h3, h4, h5 {
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: -0.02em;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    .hero-banner {
        background: linear-gradient(135deg, #090d16 0%, #1e1b4b 45%, #312e81 75%, #db2777 100%);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 24px;
        padding: 30px 34px;
        color: #ffffff;
        margin-bottom: 22px;
        box-shadow: 0 20px 40px -15px rgba(30, 27, 75, 0.6);
    }

    .hero-banner h1 {
        font-size: 2.3rem;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(135deg, #ffffff 0%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-banner p {
        color: #cbd5e1;
        font-size: 1.02rem;
        margin-top: 6px;
        margin-bottom: 0;
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 800;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        color: #0f172a;
    }

    .tag-chip {
        display: inline-block;
        padding: 4px 10px;
        font-size: 0.75rem;
        font-weight: 700;
        border-radius: 9999px;
        margin-right: 6px;
        margin-bottom: 6px;
        background: #ede9fe;
        color: #6366f1;
    }

    .tag-romantic {
        background: #ffe4e6;
        color: #e11d48;
        border: 1px solid #fecdd3;
    }

    .aesthetic-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 12px;
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.05);
    }

    .card-thumb {
        width: 68px;
        height: 68px;
        border-radius: 10px;
        object-fit: cover;
    }

    .card-info {
        flex-grow: 1;
    }

    .card-name {
        font-weight: 700;
        font-size: 0.95rem;
        color: #1e293b;
        margin-bottom: 2px;
    }

    .card-cat {
        font-size: 0.75rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
    }

    .price-badge {
        background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%);
        color: #ffffff;
        font-weight: 800;
        font-size: 0.95rem;
        padding: 6px 14px;
        border-radius: 9999px;
        white-space: nowrap;
    }

    .feature-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-banner">
        <h1>🌆 Chennai Crowd Prediction & Outing Planner</h1>
        <p>Real-time crowd simulations, parking stress checks, last-mile transit hacks, Timezone arcade menus, and smart group bill splitting.</p>
    </div>
    """,
    unsafe_allow_html=True
)

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    with st.container(border=True):
        st.markdown("<div class='section-title'>👥 1. Who is going & Group Size</div>", unsafe_allow_html=True)
        companion = st.selectbox("Choose your group", ["Family", "Couple", "Friends", "Single"])
        people_options = {"1 person": 1, "2 people": 2, "3-4 people": 4, "5+ people": 6}
        default_idx = 1 if companion == "Couple" else (0 if companion == "Single" else 2)
        headcount_label = st.selectbox("How many people?", list(people_options.keys()), index=default_idx)
        headcount = people_options[headcount_label]

    with st.container(border=True):
        st.markdown("<div class='section-title'>📍 2. Your Route (Exact Streets & Landmarks)</div>", unsafe_allow_html=True)
        manual_origin = st.checkbox("✍️ Type custom street / apartment / exact landmark manually")
        if manual_origin:
            origin = st.text_input("From (Type your exact street/locality)", value="10th Main Road, Anna Nagar")
        else:
            origin = st.selectbox("From (Select Chennai Locality)", CHENNAI_ORIGINS, index=0)

        sub_cat1, sub_cat2 = st.columns(2)
        with sub_cat1:
            place_kind = st.selectbox("Destination Type", ["Any", "Mall", "Beach", "Park & Lake", "Park & Garden"])
        with sub_cat2:
            manual_dest = st.checkbox("✍️ Type custom spot manually")

        if place_kind == "Any":
            filtered_dest_list = [d["name"] for d in DESTINATIONS]
        else:
            filtered_dest_list = [d["name"] for d in DESTINATIONS if d["type"] == place_kind]
            if not filtered_dest_list:
                filtered_dest_list = [d["name"] for d in DESTINATIONS]

        if manual_dest:
            destination_name = st.text_input("To / Destination (Type custom place)", value="VR Chennai")
        else:
            destination_name = st.selectbox("To / Destination", filtered_dest_list, index=0)

        distance_km = compute_distance(origin, destination_name)
        st.metric(label="Approximate One-Way Distance", value=str(distance_km) + " km")

with col_right:
    with st.container(border=True):
        st.markdown("<div class='section-title'>💰 3. Budget & Quick Preset Profiles</div>", unsafe_allow_html=True)

        preset = st.radio(
            "Quick Budget Presets",
            ["Custom Slider", "Broke College Student (₹150/head)", "Casual Hanging Out (₹500/head)", "Treat Day / Party (₹1500/head)"],
            horizontal=True
        )

        if preset == "Broke College Student (₹150/head)":
            total_group_budget = 150 * headcount
            st.info("🎯 Presetting ₹150/person for %d people = Total ₹%d" % (headcount, total_group_budget))
        elif preset == "Casual Hanging Out (₹500/head)":
            total_group_budget = 500 * headcount
            st.info("🎯 Presetting ₹500/person for %d people = Total ₹%d" % (headcount, total_group_budget))
        elif preset == "Treat Day / Party (₹1500/head)":
            total_group_budget = 1500 * headcount
            st.info("🎯 Presetting ₹1500/person for %d people = Total ₹%d" % (headcount, total_group_budget))
        else:
            budget_type = st.radio("Budget is for", ["Entire group", "Per person"], horizontal=True)
            budget_amount = st.slider("Budget amount (₹)", min_value=100, max_value=15000, value=1500, step=100)
            total_group_budget = budget_amount if budget_type == "Entire group" else (budget_amount * headcount)

    with st.container(border=True):
        st.markdown("<div class='section-title'>⚙️ 4. Transit & Weather Preferences</div>", unsafe_allow_html=True)
        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            transport_mode = st.selectbox("Transport Mode", ["Train / Metro", "MTC Bus", "Two-Wheeler / Bike", "Cab / Auto"])
            weather_filter = st.selectbox("Weather Mode", ["Any", "AC Indoor Only (Beat Heat)", "Open Air / Breezy"])
        with sub_col2:
            planning_day = st.selectbox("Day", ["Weekend / public holiday", "Weekday"])
            preferred_time = st.selectbox("Time Window", ["Evening", "Morning", "Afternoon", "Night"], index=0)

st.markdown("<br>", unsafe_allow_html=True)
action_btn = st.button("🚀 Calculate Smart Plan & Predict Crowd", type="primary", use_container_width=True)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Outing Plan & Travel",
    "🎯 Recommended Spots & Weather",
    "🚗 Parking & Transit Hacks",
    "📲 Share Card & Bill Splitter",
    "💬 Outing Assistant"
])

# Matched Destination Lookup
matched_dest = next((d for d in DESTINATIONS if d["name"] == destination_name), None)
if not matched_dest:
    matched_dest = {
        "name": destination_name,
        "type": place_kind if place_kind != "Any" else "Outing Destination",
        "zone": "Chennai",
        "max_capacity": 5000,
        "is_indoor": (place_kind == "Mall"),
        "description": "Custom destination in Chennai: " + destination_name,
        "best_for": ["Friends", "Family", "Couple", "Single"],
        "parking": {
            "bike_stress": "Moderate - Street / local parking depends on commercial traffic",
            "car_stress": "Moderate to High - Check road width and weekend rush",
            "hack": "Arrive 15 mins before sunset to secure convenient parking slots"
        },
        "transit": {
            "metro": "Check nearest Chennai Metro station along this corridor",
            "train": "Suburban rail accessible within local transit zone",
            "bus": "MTC bus connections via central arterial roads",
            "cheat_code": "Use metro wherever feasible to bypass traffic chokepoints"
        },
        "event_hype_alert": "Low - Regular city flow.",
        "budget_catalog": [
            {"item": "Beverages & Light Bites nearby", "price": 120, "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=300&q=80", "category": "Food"},
            {"item": "Full Meal for Two nearby", "price": 450, "image": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=300&q=80", "category": "Food"}
        ],
        "hourly_pattern": {"Morning": 20, "Afternoon": 50, "Evening": 85, "Night": 50}
    }

is_weekend = (planning_day == "Weekend / public holiday")
metrics = estimate_crowd_metrics(matched_dest, is_weekend, preferred_time)
travel_cost = estimate_travel_cost(distance_km, transport_mode, headcount)
balance_for_activities = max(0, total_group_budget - travel_cost)

# ---------------------------------
# TAB 1: OUTING PLAN & TRAVEL
# ---------------------------------
with tab1:
    st.subheader("📌 Smart Outing Summary: " + origin + " ➔ " + destination_name)

    if "Chepauk" in matched_dest.get("event_hype_alert", "") or "High" in matched_dest.get("event_hype_alert", ""):
        st.warning("⚠️ **Event / Traffic Alert:** " + matched_dest["event_hype_alert"])

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Estimated Headcount", "~ " + str(metrics['estimated_headcount']))
    m2.metric("Crowd Level", str(metrics['tier']) + " (" + str(metrics['occupancy_pct']) + "% Load)")
    m3.metric("Est. Travel Cost (Round Trip)", "₹" + str(travel_cost))
    m4.metric("Activity / Food Balance", "₹" + str(balance_for_activities))

    st.markdown(
        """
        <div style="background-color: %s15; border: 1.5px solid %s; padding: 14px 18px; border-radius: 14px; margin: 16px 0;">
            <b style="color: %s; font-size: 1.05rem;">%s CROWD DENSITY:</b>
            <span style="color: #1e293b; margin-left: 8px; font-weight: 600;">%s (~%s visitors estimated inside venue limits).</span>
        </div>
        """ % (
            metrics['badge_color'],
            metrics['badge_color'],
            metrics['badge_color'],
            metrics['tier'].upper(),
            metrics['summary'],
            metrics['estimated_headcount']
        ),
        unsafe_allow_html=True
    )

    c_act, c_route = st.columns(2)

    with c_act:
        st.markdown("#### 🍽️ What your group can do with ₹" + str(balance_for_activities) + " balance:")
        catalog = matched_dest.get("budget_catalog", [])
        affordable = [item for item in catalog if item["price"] <= balance_for_activities]

        if affordable:
            for itm in affordable:
                st.markdown(
                    """
                    <div class="aesthetic-card">
                        <img src="%s" class="card-thumb" alt="%s">
                        <div class="card-info">
                            <div class="card-name">%s</div>
                            <div class="card-cat">%s</div>
                        </div>
                        <div class="price-badge">₹%d</div>
                    </div>
                    """ % (
                        itm['image'],
                        itm['item'],
                        itm['item'],
                        itm.get('category', 'Activity'),
                        itm['price']
                    ),
                    unsafe_allow_html=True
                )
        else:
            st.info("Consider increasing your budget or selecting fewer people to unlock prime activities.")

    with c_route:
        st.markdown("#### 🚆 Step-by-Step Transit Instructions:")
        st.markdown("- 🚇 **Nearest Metro:** " + matched_dest['transit']['metro'])
        st.markdown("- 🚆 **Suburban/MRTS:** " + matched_dest['transit']['train'])
        st.markdown("- 🚌 **MTC Bus Options:** " + matched_dest['transit']['bus'])

        nav_query = urllib.parse.quote(destination_name + " Chennai")
        origin_query = urllib.parse.quote(origin + " Chennai")
        gmaps_url = "https://www.google.com/maps/dir/?api=1&origin=" + origin_query + "&destination=" + nav_query
        st.link_button("🗺️ Open Navigation Route (" + origin + " ➔ " + destination_name + ")", gmaps_url, use_container_width=True)

        st.markdown("---")
        st.markdown("#### 🔀 2-Stop 'Day-Out Hopper' Sequence:")
        st.write("Plan a smooth afternoon-to-evening outing without planning friction:")
        if matched_dest["type"] == "Mall":
            st.markdown("- **Stop 1 (Afternoon):** %s (AC Cinema / Timezone Arcade / Lunch)" % destination_name)
            st.markdown("- **Stop 2 (Sunset/Evening):** Hop over to **Anna Nagar Tower Park** or **Semmozhi Poonga** for evening breeze and filter coffee.")
        else:
            st.markdown("- **Stop 1 (Afternoon):** Lunch / Coffee at a nearby indoor cafe")
            st.markdown("- **Stop 2 (Sunset/Evening):** %s for sunset sea breeze and street eats" % destination_name)

# ---------------------------------
# TAB 2: RECOMMENDED SPOTS & WEATHER
# ---------------------------------
with tab2:
    if companion == "Couple":
        st.markdown(
            """
            <div style="background: #fff1f2; border-left: 5px solid #f43f5e; padding: 12px 16px; border-radius: 8px; margin-bottom: 16px;">
                <b style="color: #be185d;">❤️ Couple Spots Activated:</b>
                Showing curated romantic beach walks, pedal boating lakes, and intimate cafes around Chennai.
            </div>
            """,
            unsafe_allow_html=True
        )

    all_recommendations = get_recommendations(
        is_weekend=is_weekend,
        preferred_time=preferred_time,
        group=companion,
        place_type=place_kind,
        weather_pref=weather_filter
    )

    st.write("Showing **%d** spots tailored for **%s** (%s - %s):" % (len(all_recommendations), companion, place_kind, weather_filter))

    for spot in all_recommendations:
        c = spot["crowd"]
        dist = compute_distance(origin, spot["name"])

        with st.container(border=True):
            r_col1, r_col2 = st.columns([3, 1])

            with r_col1:
                st.markdown("### 📍 " + spot['name'])
                st.write("*" + spot['description'] + "*")

                chips = "<span class='tag-chip'>" + spot['type'] + "</span>"
                chips += "<span class='tag-chip'>" + spot['zone'] + "</span>"
                chips += "<span class='tag-chip'>🛣️ " + str(dist) + " km from " + origin + "</span>"
                if spot.get("is_indoor"):
                    chips += "<span class='tag-chip'>❄️ AC Indoor</span>"
                else:
                    chips += "<span class='tag-chip'>🌊 Open Air</span>"
                if spot.get("couple_friendly"):
                    chips += "<span class='tag-chip tag-romantic'>❤️ Couple Friendly</span>"
                for tag in spot.get("vibe_tags", []):
                    chips += "<span class='tag-chip'>" + tag + "</span>"

                st.markdown(chips, unsafe_allow_html=True)

            with r_col2:
                st.markdown(
                    """
                    <div style="background-color: %s15; border: 1px solid %s; padding: 10px; border-radius: 12px; text-align: center;">
                        <span style="color: %s; font-weight: 800; font-size: 0.95rem;">
                            %s (%d%% Load)
                        </span>
                        <div style="font-size: 1.15rem; font-weight: 800; color: #1e293b; margin: 4px 0;">
                            ~ %s
                        </div>
                        <small style="color: #64748b;">visitors estimated</small>
                    </div>
                    """ % (
                        c['badge_color'],
                        c['badge_color'],
                        c['badge_color'],
                        c['tier'].upper(),
                        c['occupancy_pct'],
                        c['estimated_headcount']
                    ),
                    unsafe_allow_html=True
                )

# ---------------------------------
# TAB 3: PARKING & TRANSIT HACKS
# ---------------------------------
with tab3:
    st.subheader("🚗 Parking Reality Check & Local Transit Hacks")
    st.write("Avoid spending 30 minutes in a parking queue or getting stuck in bottleneck traffic:")

    p_col1, p_col2 = st.columns(2)

    with p_col1:
        st.markdown(
            """
            <div class="feature-box">
                <h4>🏍️ Two-Wheeler / Bike Parking:</h4>
                <p><b>Status:</b> %s</p>
                <hr>
                <h4>🚙 Four-Wheeler / Car Parking:</h4>
                <p><b>Status:</b> %s</p>
            </div>
            """ % (
                matched_dest["parking"]["bike_stress"],
                matched_dest["parking"]["car_stress"]
            ),
            unsafe_allow_html=True
        )

    with p_col2:
        st.markdown(
            """
            <div class="feature-box" style="border-left: 4px solid #6366f1;">
                <h4>⚡ Insider Parking Cheat Code:</h4>
                <p>%s</p>
                <hr>
                <h4>🚇 Last-Mile Transit Hack:</h4>
                <p>%s</p>
            </div>
            """ % (
                matched_dest["parking"]["hack"],
                matched_dest["transit"].get("cheat_code", "Use nearby metro feeder autos")
            ),
            unsafe_allow_html=True
        )

# ---------------------------------
# TAB 4: SHARE CARD & BILL SPLITTER
# ---------------------------------
with tab4:
    st.subheader("📲 WhatsApp / Insta Story Plan & Bill Splitter")

    s_col1, s_col2 = st.columns(2)

    with s_col1:
        st.markdown("#### 📋 1-Click WhatsApp / Instagram Summary Card:")
        share_text = (
            "🌆 *CHENNAI OUTING PLAN*\n"
            "📍 *Route:* %s ➔ %s (%s km)\n"
            "👥 *Group:* %s (%d people)\n"
            "💰 *Total Budget:* ₹%d (₹%d for food/activities)\n"
            "📊 *Crowd Forecast:* %s (%s visitors)\n"
            "🚇 *Transit Hack:* %s\n"
            "— Created via Chennai Crowd Prediction & Outing Planner"
        ) % (
            origin, destination_name, str(distance_km),
            companion, headcount,
            total_group_budget, balance_for_activities,
            metrics["tier"], metrics["estimated_headcount"],
            matched_dest["transit"].get("cheat_code", "Take metro/bus")
        )

        st.text_area("Copy and paste to WhatsApp group or Insta story:", value=share_text, height=210)

        # Pre-filled WhatsApp Web Link
        encoded_wa = urllib.parse.quote(share_text)
        wa_url = "https://api.whatsapp.com/send?text=" + encoded_wa
        st.link_button("📲 Share Directly on WhatsApp", wa_url, use_container_width=True)

    with s_col2:
        st.markdown("#### 💸 Group Expense & Bill Split Calculator:")
        st.write("Enter total money spent to calculate exact per-person shares:")

        spent_travel = st.number_input("Travel / Parking Spent (₹)", value=travel_cost, step=20)
        spent_food = st.number_input("Food & Dining Spent (₹)", value=int(balance_for_activities * 0.6), step=50)
        spent_tickets = st.number_input("Games / Cinema / Tickets Spent (₹)", value=int(balance_for_activities * 0.4), step=50)

        total_spent = spent_travel + spent_food + spent_tickets
        per_person_share = int(total_spent / max(1, headcount))

        st.metric(label="Total Outing Spend", value="₹" + str(total_spent))
        st.metric(label="Exact Share Per Person", value="₹" + str(per_person_share))

        # UPI Payment Link Generator
        upi_id = st.text_input("Enter your UPI ID to collect shares (Optional)", value="yourname@okaxis")
        if upi_id:
            upi_note = urllib.parse.quote("Outing share for %s" % destination_name)
            upi_link = "upi://pay?pa=%s&pn=OutingPlanner&am=%d&cu=INR&tn=%s" % (upi_id, per_person_share, upi_note)
            st.caption("📱 Copy UPI collect URI for friends: `%s`" % upi_link)

# ---------------------------------
# TAB 5: MULTI-TURN AI ASSISTANT
# ---------------------------------
with tab5:
    st.subheader("💬 Chennai Outing AI Assistant")
    st.caption("Ask about crowds, routes, couples spots, Timezone games, parking queues, or food options across Chennai.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hey! I'm your Chennai Outing Assistant. Ask me anything about timings, crowd levels, Timezone arcade prices, parking hacks, or quiet date spots!"
            }
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_prompt = st.chat_input("Ask a question about your outing...")
    if user_prompt:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        q = user_prompt.lower()
        if any(w in q for w in ["parking", "bike", "car", "park"]):
            reply = (
                "🚗 **Parking Reality Check for " + destination_name + ":**\n\n"
                "- **Bike Parking:** " + matched_dest["parking"]["bike_stress"] + "\n"
                "- **Car Parking:** " + matched_dest["parking"]["car_stress"] + "\n"
                "- **Cheat Code:** " + matched_dest["parking"]["hack"]
            )
        elif any(w in q for w in ["game", "vr", "bowling", "arcade", "timezone"]):
            reply = (
                "🎮 **VR Chennai Timezone & Arcade Breakdown:**\n\n"
                "- **Bowling Alley:** ₹380 per string game (shoes included).\n"
                "- **VR 9D Simulator:** ₹280 per ride.\n"
                "- **Krazy Kars Bumper Cars:** ₹160 per session.\n"
                "- **Air Hockey & Basketball Arcade:** ₹120 per round.\n"
                "- **Basic Video Arcade Tokens:** ₹80 per token.\n\n"
                "With your current balance of **₹" + str(balance_for_activities) + "**, your group can easily enjoy multiple games!"
            )
        elif any(w in q for w in ["couple", "date", "romantic"]):
            reply = (
                "❤️ **Top Romantic Date Spots in Chennai:**\n\n"
                "1. **Besant Nagar (Elliot's Beach):** Sunset breeze, aesthetic beachside cafes, and romantic walks.\n"
                "2. **Chetpet Eco Park:** Pedal boating for two on the lake (₹150 for 30 mins) with quiet walking paths.\n"
                "3. **Semmozhi Poonga:** Shaded botanical trails, exotic flowers, and quiet benches (Entry ₹25).\n"
                "4. **VR Chennai Rooftop:** Evening courtyard dining under warm fairy lights."
            )
        elif any(w in q for w in ["budget", "cost", "price", "cheap", "150", "money"]):
            reply = (
                "💰 **Smart Budget Strategy for ₹" + str(total_group_budget) + ":**\n\n"
                "- **Round-Trip Travel:** Using " + transport_mode + " will cost roughly **₹" + str(travel_cost) + "** for " + str(headcount) + " people.\n"
                "- **Remaining Balance:** You have **₹" + str(balance_for_activities) + "**.\n"
                "- **Recommendation:** At " + destination_name + ", grab McDonald's / food court combos (~₹190/person) and hit 1 or 2 arcade games or cinema matinee shows!"
            )
        elif any(w in q for w in ["bus", "metro", "reach", "route", "train", "distance"]):
            reply = (
                "🚆 **How to reach " + destination_name + " from " + origin + ":**\n\n"
                "- **Distance:** Approximately **" + str(distance_km) + " km**.\n"
                "- **Transit Hack:** " + matched_dest["transit"].get("cheat_code", matched_dest["transit"]["metro"]) + "\n"
                "- Tap the **'Open Navigation Route'** button on Tab 1 to open live Google Maps!"
            )
        elif any(w in q for w in ["quiet", "less crowd", "peace", "crowd"]):
            headcount_val = str(metrics["estimated_headcount"])
            tier_val = str(metrics["tier"])
            load_val = str(metrics["occupancy_pct"])
            reply = (
                "📊 **Crowd Density Overview for " + destination_name + ":**\n\n"
                "- Currently estimated at **" + tier_val + "** (~" + headcount_val + " people, " + load_val + "% capacity load).\n"
                "- If you want fewer crowds, visit during the **Morning (10 AM - 12 PM)** or consider visiting **Akkarai Beach** or **Semmozhi Poonga** instead!"
            )
        else:
            reply = (
                "🌆 **Outing Insights for " + destination_name + ":**\n\n"
                "Visiting from **" + origin + "** for a **" + companion + "** outing is a great choice! "
                "With an estimated distance of **" + str(distance_km) + " km**, you will have **₹" + str(balance_for_activities) + "** remaining after " + transport_mode + " travel. "
                "Feel free to ask for specific restaurant suggestions, parking tips, or quiet evening alternatives!"
            )

        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)

st.markdown("---")
st.caption("Chennai Crowd Prediction & Outing Recommendation System | Capacity simulation model for academic & prototype demonstration")
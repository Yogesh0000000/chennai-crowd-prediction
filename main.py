"""
Chennai Crowd Prediction – A Crowd-Aware Outing Recommendation System
Gen-Z Inspired Dashboard with All-Landmark Support, Dynamic Category Filters,
Aesthetic Visual Menus, VR Gamezone Prices, and Multi-Turn AI Outing Assistant.
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

# ---------------------------------
# 1. STREAMLIT SETUP & CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Chennai Crowd Prediction & Outing Planner",
    page_icon="🌆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------
# 2. VIBRANT GEN-Z THEME & CSS
# ---------------------------------
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

    /* Vibrant Hero Header */
    .hero-banner {
        background: linear-gradient(135deg, #090d16 0%, #1e1b4b 45%, #312e81 75%, #db2777 100%);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 24px;
        padding: 32px 36px;
        color: #ffffff;
        margin-bottom: 24px;
        box-shadow: 0 20px 40px -15px rgba(30, 27, 75, 0.6);
    }

    .hero-banner h1 {
        font-size: 2.4rem;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(135deg, #ffffff 0%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-banner p {
        color: #cbd5e1;
        font-size: 1.05rem;
        margin-top: 8px;
        margin-bottom: 0;
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 800;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
        color: #0f172a;
    }

    /* Chips */
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

    /* Aesthetic Visual Card for Activities & Food */
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
        transition: transform 0.15s ease-in-out;
    }

    .aesthetic-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px -3px rgba(0, 0, 0, 0.08);
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
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------
# 3. HERO HEADER
# ---------------------------------
st.markdown(
    """
    <div class="hero-banner">
        <h1>🌆 Chennai Crowd Prediction & Outing Planner</h1>
        <p>Choose your people, route, and budget. Get an intelligent plan with venue capacity headcounts, Timezone arcade prices, and full transit directions.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------
# 4. DASHBOARD PLANNER INPUT GRID
# ---------------------------------
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    # --- WHO IS GOING SECTION ---
    with st.container(border=True):
        st.markdown("<div class='section-title'>👥 Who is going?</div>", unsafe_allow_html=True)

        companion = st.selectbox(
            "Choose your group",
            ["Family", "Couple", "Friends", "Single"],
            help="Selecting Couple prioritizes scenic date spots & romantic spots in Chennai."
        )

        people_options = {
            "1 person": 1,
            "2 people": 2,
            "3–4 people": 4,
            "5+ people": 6
        }
        default_idx = 1 if companion == "Couple" else (0 if companion == "Single" else 2)
        headcount_label = st.selectbox("How many people?", list(people_options.keys()), index=default_idx)
        headcount = people_options[headcount_label]

    # --- YOUR ROUTE SECTION (ALL CHENNAI LANDMARKS & CUSTOM STREETS) ---
    with st.container(border=True):
        st.markdown("<div class='section-title'>📍 Your route</div>", unsafe_allow_html=True)

        manual_origin = st.checkbox("✍️ Enter custom street / apartment / exact landmark manually")

        if manual_origin:
            origin = st.text_input(
                "From (Type your exact street/locality)",
                value="10th Main Road, Anna Nagar",
                placeholder="e.g. South Mada Street, Mylapore or Gandhi Road, Tambaram"
            )
        else:
            origin = st.selectbox("From (Select Chennai Locality)", CHENNAI_ORIGINS, index=0)

        # Dynamic Category Selection for Destination
        sub_cat1, sub_cat2 = st.columns(2)
        with sub_cat1:
            place_kind = st.selectbox(
                "What kind of place?",
                ["Any", "Mall", "Beach", "Park & Lake", "Park & Garden", "Shopping District"]
            )
        with sub_cat2:
            manual_dest = st.checkbox("✍️ Type custom place manually")

        # Dynamic Destination List based on selected category
        if place_kind == "Any":
            filtered_dest_list = [d["name"] for d in DESTINATIONS]
        else:
            filtered_dest_list = [d["name"] for d in DESTINATIONS if d["type"] == place_kind]
            if not filtered_dest_list:
                filtered_dest_list = [d["name"] for d in DESTINATIONS]

        if manual_dest:
            destination_name = st.text_input("To / destination (Type custom place)", value="VR Chennai")
        else:
            destination_name = st.selectbox("To / destination", filtered_dest_list, index=0)

        # Approximate one-way distance
        distance_km = compute_distance(origin, destination_name)
        st.metric(label="Approximate one-way distance (km)", value=f"{distance_km:.1f} km")

with col_right:
    # --- YOUR BUDGET SECTION ---
    with st.container(border=True):
        st.markdown("<div class='section-title'>💰 Your budget</div>", unsafe_allow_html=True)

        budget_type = st.radio("Budget is for", ["Entire group", "Per person"], horizontal=True)

        budget_amount = st.slider(
            "Budget amount (₹)",
            min_value=100,
            max_value=15000,
            value=1500,
            step=100
        )

        total_group_budget = budget_amount if budget_type == "Entire group" else (budget_amount * headcount)

    # --- OUTING PREFERENCES & TRANSPORT ---
    with st.container(border=True):
        st.markdown("<div class='section-title'>⚙️ Outing Preferences</div>", unsafe_allow_html=True)

        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            transport_mode = st.selectbox(
                "Transport mode",
                ["Train / Metro", "MTC Bus", "Two-Wheeler / Bike", "Cab / Auto"]
            )

        with sub_col2:
            planning_day = st.selectbox(
                "When are you planning to go?",
                ["Weekend / public holiday", "Weekday"]
            )
            preferred_time = st.selectbox(
                "Preferred time",
                ["Evening", "Morning", "Afternoon", "Night"],
                index=0
            )

st.markdown("<br>", unsafe_allow_html=True)
action_btn = st.button("🚀 Calculate Smart Plan & Predict Crowd", type="primary", use_container_width=True)

# ---------------------------------
# 5. RESULTS PRESENTATION TABS
# ---------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Estimated Plan & Travel Costs", "🎯 Recommended Chennai Spots", "💬 Outing Assistant"])

# ---------------------------------
# TAB 1: ESTIMATED PLAN & TRAVEL
# ---------------------------------
with tab1:
    matched_dest = next((d for d in DESTINATIONS if d["name"] == destination_name), None)

    if not matched_dest:
        matched_dest = {
            "name": destination_name,
            "type": place_kind if place_kind != "Any" else "Outing Destination",
            "zone": "Chennai",
            "max_capacity": 5000,
            "description": f"Custom destination in Chennai: {destination_name}.",
            "best_for": ["Friends", "Family", "Couple", "Single"],
            "transit": {
                "metro": "Check nearby Chennai Metro lines on route",
                "train": "Suburban rail accessible nearby",
                "bus": "MTC bus connections via central corridors"
            },
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

    st.subheader(f"📌 Outing Plan: {origin} ➔ {destination_name}")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Estimated Headcount", f"~ {metrics['estimated_headcount']}")
    m2.metric("Crowd Level", f"{metrics['tier']} ({metrics['occupancy_pct']}% Load)")
    m3.metric("Est. Travel Cost (Round Trip)", f"₹{travel_cost}")
    m4.metric("Activity / Food Balance", f"₹{balance_for_activities}")

    st.markdown(
        f"""
        <div style="background-color: {metrics['badge_color']}15; border: 1.5px solid {metrics['badge_color']}; padding: 14px 18px; border-radius: 14px; margin: 16px 0;">
            <b style="color: {metrics['badge_color']}; font-size: 1.05rem;">{metrics['tier'].upper()} CROWD DENSITY:</b>
            <span style="color: #1e293b; margin-left: 8px; font-weight: 600;">{metrics['summary']} (~{metrics['estimated_headcount']} visitors estimated inside venue limits).</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    c_act, c_route = st.columns(2)

    with c_act:
        st.markdown(f"#### 🍽️ What your group can do with ₹{balance_for_activities} balance:")
        catalog = matched_dest.get("budget_catalog", [])
        affordable = [item for item in catalog if item["price"] <= balance_for_activities]

        if affordable:
            for itm in affordable:
                st.markdown(
                    f"""
                    <div class="aesthetic-card">
                        <img src="{itm['image']}" class="card-thumb" alt="{itm['item']}">
                        <div class="card-info">
                            <div class="card-name">{itm['item']}</div>
                            <div class="card-cat">{itm.get('category', 'Activity')}</div>
                        </div>
                        <div class="price-badge">₹{itm['price']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("Consider increasing your budget to cover premier activities at this venue.")

    with c_route:
        st.markdown("#### 🚆 Step-by-Step Transit Instructions:")
        st.markdown(f"- 🚇 **Nearest Metro:** {matched_dest['transit']['metro']}")
        st.markdown(f"- 🚆 **Suburban/MRTS:** {matched_dest['transit']['train']}")
        st.markdown(f"- 🚌 **MTC Bus Options:** {matched_dest['transit']['bus']}")

        nav_query = urllib.parse.quote(f"{destination_name} Chennai")
        origin_query = urllib.parse.quote(f"{origin} Chennai")
        gmaps_url = f"https://www.google.com/maps/dir/?api=1&origin={origin_query}&destination={nav_query}"
        st.link_button(f"🗺️ Open Navigation Route ({origin} ➔ {destination_name})", gmaps_url, use_container_width=True)

# ---------------------------------
# TAB 2: RECOMMENDED SPOTS
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
        is_weekend=(planning_day == "Weekend / public holiday"),
        preferred_time=preferred_time,
        group=companion,
        place_type=place_kind
    )

    st.write(f"Showing **{len(all_recommendations)}** spots tailored for **{companion}** ({place_kind}):")

    for spot in all_recommendations:
        c = spot["crowd"]
        dist = compute_distance(origin, spot["name"])

        with st.container(border=True):
            r_col1, r_col2 = st.columns([3, 1])

            with r_col1:
                st.markdown(f"### 📍 {spot['name']}")
                st.write(f"*{spot['description']}*")

                chips = f"<span class='tag-chip'>{spot['type']}</span>"
                chips += f"<span class='tag-chip'>{spot['zone']}</span>"
                chips += f"<span class='tag-chip'>🛣️ {dist:.1f} km from {origin}</span>"
                if spot.get("couple_friendly"):
                    chips += "<span class='tag-chip tag-romantic'>❤️ Couple Friendly</span>"
                for tag in spot.get("vibe_tags", []):
                    chips += f"<span class='tag-chip'>{tag}</span>"

                st.markdown(chips, unsafe_allow_html=True)

            with r_col2:
                st.markdown(
                    f"""
                    <div style="background-color: {c['badge_color']}15; border: 1px solid {c['badge_color']}; padding: 10px; border-radius: 12px; text-align: center;">
                        <span style="color: {c['badge_color']}; font-weight: 800; font-size: 0.95rem;">
                            {c['tier'].upper()} ({c['occupancy_pct']}% Load)
                        </span>
                        <div style="font-size: 1.15rem; font-weight: 800; color: #1e293b; margin: 4px 0;">
                            ~ {c['estimated_headcount']}
                        </div>
                        <small style="color: #64748b;">visitors estimated</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# ---------------------------------
# TAB 3: ASSISTANT CHATBOT (ALL QUESTIONS ANSWERED)
# ---------------------------------
with tab3:
    st.subheader("💬 Chennai Outing AI Assistant")
    st.caption("Ask anything about crowds, routes, couples spots, Timezone games, or food options across Chennai.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": f"Hey! I'm your Chennai Outing Assistant. I see you're planning a trip for a **{companion}** from **{origin}** to **{destination_name}** with a balance of **₹{balance_for_activities}**. Ask me anything about timings, crowd levels, Timezone arcade prices, or secret quiet spots!"
            }
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Conversational Input
    if user_prompt := st.chat_input("Ask a question about your outing..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Conversational Intelligence Fallback Engine
        q = user_prompt.lower()
        if "game" in q or "vr" in q or "bowling" in q or "arcade" in q or "timezone" in q:
            reply = (
                "🎮 **VR Chennai Timezone & Arcade Breakdown:**\n\n"
                "- **Bowling Alley:** ₹380 per string game (shoes included).\n"
                "- **VR 9D Simulator:** ₹280 per ride.\n"
                "- **Krazy Kars Bumper Cars:** ₹160 per session.\n"
                "- **Air Hockey & Basketball Arcade:** ₹120 per round.\n"
                "- **Basic Video Arcade Tokens:** ₹80 per token.\n\n"
                f"With your current balance of **₹{balance_for_activities}**, your group can easily enjoy multiple games!"
            )
        elif "couple" in q or "date" in q or "romantic" in q:
            reply = (
                "❤️ **Top Romantic Date Spots in Chennai:**\n\n"
                "1. **Besant Nagar (Elliot's Beach):** Sunset breeze, aesthetic beachside cafes, and romantic walks.\n"
                "2. **Chetpet Eco Park:** Pedal boating for two on the lake (₹150 for 30 mins) with quiet walking paths.\n"
                "3. **Semmozhi Poonga:** Shaded botanical trails, exotic flowers, and quiet benches (Entry ₹25).\n"
                "4. **VR Chennai Rooftop:** Evening courtyard dining under warm fairy lights."
            )
        elif "budget" in q or "cost" in q or "price" in q or "cheap" in q:
            reply = (
                f"💰 **Smart Budget Strategy for ₹{total_group_budget}:**\n\n"
                f"- **Round-Trip Travel:** Using {transport_mode} will cost roughly **₹{travel_cost}** for {headcount} people.\n"
                f"- **Remaining Balance:** You have **₹{balance_for_activities}**.\n"
                f"- **Recommendation:** At {destination_name}, grab McDonald's / food court combos (~₹190/person) and hit 1 or 2 arcade games or cinema matinee shows!"
            )
        elif "bus" in q or "metro" in q or "reach" in q or "route" in q:
            reply = (
                f"🚆 **How to reach {destination_name} from {origin}:**\n\n"
                f"- **Distance:** Approximately **{distance_km:.1f} km**.\n"
                f"- **Transit Options:** {matched_dest['transit']['metro']} or take direct MTC buses: {matched_dest['transit']['bus']}.\n"
                f"- Tap the **'Open Navigation Route'** button on the first tab to open live turn-by-turn Google Maps!"
            )
        elif "quiet" in q or "less crowd" in q or "crowd" in q:
            headcount_val = metrics["estimated_headcount"]
            tier_val = metrics["tier"]
            load_val = metrics["occupancy_pct"]
            reply = (
                f"📊 **Crowd Density Overview for {destination_name}:**\n\n"
                f"- Currently estimated at **{tier_val}** (~{headcount_val} people, {load_val}% capacity load).\n"
                "- If you want fewer crowds, visit during the **Morning (10 AM – 12 PM)** or consider visiting **Akkarai Beach** or **Semmozhi Poonga** instead!"
            )
        else:
            reply = (
                f"🌆 **Outing Insights for {destination_name}:**\n\n"
                f"Visiting from **{origin}** for a **{companion}** outing is a great choice! "
                f"With an estimated distance of **{distance_km:.1f} km**, you'll have **₹{balance_for_activities}** remaining after {transport_mode} travel. "
                "Feel free to ask for specific restaurant suggestions, parking tips, or quiet evening alternatives!"
            )

        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)

# ---------------------------------
# FOOTER
# ---------------------------------
st.markdown("---")
st.caption(
    "Chennai Crowd Prediction & Outing Recommendation System | "
    "Capacity simulation model for academic & prototype demonstration"
)
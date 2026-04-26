import streamlit as st
import pandas as pd

# ==========================================
# 1. CSS STYLING (Aesthetic Mobile UI)
# ==========================================
st.set_page_config(page_title="Petizen", page_icon="🐾", layout="centered")

st.markdown("""
    <style>
    /* Global Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #FFF5F5 0%, #FFFFFF 100%);
    }
    
    /* Card UI Style */
    .app-card {
        background-color: white;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.12);
        border: 1px solid #FFE3E3;
    }
    
    /* Petizen Pink Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #FF6B6B 0%, #FF8E8E 100%);
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        font-weight: bold;
        transition: 0.3s;
        height: 48px;
        width: 100%;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
    }
    
    /* Merchant UI */
    .shop-title { font-size: 22px; font-weight: bold; color: #2D3436; }
    .shop-tag { background: #FFF0F0; color: #FF6B6B; padding: 4px 10px; border-radius: 8px; font-size: 12px; margin-right: 5px; font-weight: 600; }
    
    /* Social Media Style */
    .post-user { font-weight: bold; color: #FF6B6B; font-size: 16px; }
    .comment-box { background: #F8F9FA; padding: 12px; border-radius: 12px; margin-top: 8px; font-size: 14px; border-left: 3px solid #FF6B6B; }
    .action-btn { border: 1px solid #FF6B6B; background: white; color: #FF6B6B; border-radius: 15px; padding: 3px 12px; font-size: 12px; font-weight:bold; cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. DATABASE (Using your Chinese Filenames)
# ==========================================

# 12 Merchants with Details
merchants = [
    {"id": 1, "name": "Fancy Tail Spa", "loc": "Central", "dist": 0.5, "price": 450, "rating": 4.9, "img": "商店1.jpg", "tel": "2345 1001", "serv": "Pet Haircut, Milk Bath, Grooming"},
    {"id": 2, "name": "CityVet Health", "loc": "Wan Chai", "dist": 1.2, "price": 850, "rating": 4.8, "img": "商店2.jpg", "tel": "2345 1002", "serv": "Medical Hospital, Vaccine, Checkup"},
    {"id": 3, "name": "Paws Coffee", "loc": "Causeway Bay", "dist": 0.8, "price": 120, "rating": 4.7, "img": "商店3.jpg", "tel": "2345 1003", "serv": "Pet Afternoon Tea, Coffee Social"},
    {"id": 4, "name": "Summer Pool", "loc": "Sai Kung", "dist": 5.4, "price": 300, "rating": 4.6, "img": "商店4.jpg", "tel": "2345 1004", "serv": "Pet Swimming, Drying Service"},
    {"id": 5, "name": "Royal Paw Hotel", "loc": "Mid-Levels", "dist": 2.1, "price": 600, "rating": 5.0, "img": "商店5.jpg", "tel": "2345 1005", "serv": "24/7 Daycare, Pet Boarding"},
    {"id": 6, "name": "Elite Grooming", "loc": "Tsim Sha Tsui", "dist": 3.5, "price": 550, "rating": 4.7, "img": "商店6.jpg", "tel": "2345 1006", "serv": "Professional Styling, Nail Art"},
    {"id": 7, "name": "Pet Boutique", "loc": "Mong Kok", "dist": 4.2, "price": 200, "rating": 4.5, "img": "商店7.jpg", "tel": "2345 1007", "serv": "Pet Clothes, Accessories, Toys"},
    {"id": 8, "name": "Gentle Vet", "loc": "Shatin", "dist": 6.8, "price": 750, "rating": 4.8, "img": "商店8.jpg", "tel": "2345 1008", "serv": "Vet Clinic, Emergency Care"},
    {"id": 9, "name": "Bark & Bakery", "loc": "Stanley", "dist": 7.2, "price": 150, "rating": 4.9, "img": "商店9.jpg", "tel": "2345 1009", "serv": "Pet Bakery, Birthday Cakes"},
    {"id": 10, "name": "Cloud Care", "loc": "Kowloon Tong", "dist": 3.0, "price": 400, "rating": 4.4, "img": "商店10.jpg", "tel": "2345 1010", "serv": "Interactive Play, Daycare"},
    {"id": 11, "name": "Zen Retreat", "loc": "North Point", "dist": 2.5, "price": 80, "rating": 4.7, "img": "商店 11.jpg", "tel": "2345 1011", "serv": "Massage, Therapy, Relaxation"},
    {"id": 12, "name": "Pet Uber HK", "loc": "All Districts", "dist": 0.1, "price": 180, "rating": 5.0, "img": "商店12.jpg", "tel": "2345 1012", "serv": "Pet Taxi, Safe Transport"}
]

# 10 Group-buy Deals
coupons = [
    {"name": "Bundle: Bath + Haircut", "price": "$399", "orig": "$550", "type": "Bundle"},
    {"name": "Group Buy: Cat Food (3 Bags)", "price": "$888", "orig": "$1200", "type": "Group Buy"},
    {"name": "Vaccine & Checkup Combo", "price": "$699", "orig": "$950", "type": "Health"},
    {"name": "Afternoon Tea for 2 Pets", "price": "$199", "orig": "$320", "type": "Dining"},
    {"name": "7-Day Daycare Package", "price": "$2500", "orig": "$3500", "type": "Service"},
    {"name": "Pet Swimming (10 Entries)", "price": "$2200", "orig": "$3000", "type": "Sport"},
    {"name": "New Pet Starter Kit", "price": "$450", "orig": "$650", "type": "Combo"},
    {"name": "Full Grooming + Dental Care", "price": "$780", "orig": "$1100", "type": "VIP"},
    {"name": "Joint Spa & Massage Deal", "price": "$550", "orig": "$800", "type": "Relax"},
    {"name": "Puppy Training Bundle", "price": "$1200", "orig": "$1800", "type": "Training"}
]

# 8 Forum Posts
posts = [
    {"user": "@Kitty_Lover", "img": "宠物1.jpg", "text": "My cute kitty climbed onto my bed today!", "comments": ["So cute!", "My cat does that too!"]},
    {"user": "@CupCat_Mom", "img": "宠物2.jpg", "text": "My one-year-old cat is tiny enough to fit in a cup! So adorable.", "comments": ["A cup of kitty!", "Too tiny to be real!"]},
    {"user": "@Bunny_Sir", "img": "宠物3.jpg", "text": "My bunny actually covered its eyes while I was changing! Such a polite boy.", "comments": ["What a gentleman!", "LOL, shy bunny."]},
    {"user": "@LineFriend", "img": "宠物4.jpg", "text": "My puppy looks exactly like the Line Friends dog character!", "comments": ["Spot on!", "I want a toy like him."]},
    {"user": "@Parrot_Fan", "img": "宠物5.jpg", "text": "My little parrot's head is so round, he looks like a gentleman.", "comments": ["Very elegant!", "Smart bird."]},
    {"user": "@Alpaca_Rider", "img": "宠物6.jpg", "text": "Every time I see my alpaca, I feel the urge to jump on it!", "comments": ["Don't do it! Haha", "Iconic fluffy friend."]},
    {"user": "@Piggy_World", "img": "宠物7.jpg", "text": "Pet pigs are actually super cute too.", "comments": ["Oink oink!", "I want a mini pig!"]},
    {"user": "@Hedge_X", "img": "宠物8.jpg", "text": "The little hedgehog always messes around while I'm working.", "comments": ["Spiky coworker!", "Mine does that too!"]}
]

# ==========================================
# 3. APP LOGIC
# ==========================================

if 'nav' not in st.session_state:
    st.session_state.nav = 'Passport'

# --- PAGE: PET PASSPORT ---
if st.session_state.nav == 'Passport':
    col_logo1, col_logo2 = st.columns([1, 4])
    with col_logo1: st.image("logo.jpg", width=80)
    with col_logo2: st.markdown("<h1 style='color:#FF6B6B; margin-top:10px;'>Petizen</h1>", unsafe_allow_html=True)
    
    st.write("Welcome! Create a passport for your best friend.")
    with st.form("passport"):
        st.subheader("Pet Details")
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Pet Name *")
            st.text_input("Fur Color")
        with c2:
            st.text_input("Personality")
            st.text_input("Dietary Preference")
        
        st.subheader("Owner Contact")
        owner_name = st.text_input("Owner Name *")
        owner_tel = st.text_input("Contact Phone Number *")
        
        if st.form_submit_button("Enter Petizen World"):
            if owner_name and owner_tel:
                st.session_state.user = owner_name
                st.session_state.nav = 'Home'
                st.rerun()
            else:
                st.error("Please fill in the required fields (*).")

# --- PAGE: HOME (12 SHOPS) ---
elif st.session_state.nav == 'Home':
    st.image("logo.jpg", width=70)
    st.markdown(f"## Hello, {st.session_state.user}! 👋")
    
    sort_option = st.selectbox("Sort By:", 
                               ["Distance (Nearest)", "Rating (Highest)", 
                                "Price (Low to High)", "Price (High to Low)"])
    
    df_shops = pd.DataFrame(merchants)
    if "Distance" in sort_option: df_shops = df_shops.sort_values("dist")
    elif "Rating" in sort_option: df_shops = df_shops.sort_values("rating", ascending=False)
    elif "Low to High" in sort_option: df_shops = df_shops.sort_values("price")
    elif "High to Low" in sort_option: df_shops = df_shops.sort_values("price", ascending=False)
    
    for idx, row in df_shops.iterrows():
        with st.container():
            st.markdown(f"""
            <div class="app-card">
                <img src="{row['img']}" style="width:100%; border-radius:15px; margin-bottom:15px; height:200px; object-fit:cover;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="shop-title">{row['name']}</span>
                    <span style="color:#FF6B6B; font-weight:bold; font-size:18px;">⭐ {row['rating']}</span>
                </div>
                <div style="margin: 10px 0;">
                    <span class="shop-tag">📍 {row['loc']} ({row['dist']}km)</span>
                    <span class="shop-tag">💰 ${row['price']} up</span>
                </div>
                <p style="font-size:15px; color:#2D3436;"><b>Services:</b> {row['serv']}</p>
                <p style="font-size:13px; color:#95A5A6;">📞 Tel: {row['tel']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("Book Now", key=f"shop_{idx}")

# --- PAGE: DEALS ---
elif st.session_state.nav == 'Deals':
    st.markdown("## 🎟️ Exclusive Bundle Deals")
    st.write("Group-buy discounts for high-quality pet care.")
    for c in coupons:
        st.markdown(f"""
        <div class="app-card" style="border-left: 10px solid #FF6B6B;">
            <div style="display:flex; justify-content:space-between;">
                <span style="font-weight:bold; font-size:19px;">{c['name']}</span>
                <span style="background:#FF6B6B; color:white; padding:2px 12px; border-radius:12px; font-size:10px; font-weight:bold;">{c['type']}</span>
            </div>
            <div style="margin-top:15px;">
                <span style="font-size:26px; font-weight:bold; color:#FF6B6B;">{c['price']}</span>
                <span style="text-decoration:line-through; color:#BDC3C7; font-size:16px; margin-left:10px;">{c['orig']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button(f"Claim Bundle", key=f"deal_{c['name']}")

# --- PAGE: COMMUNITY ---
elif st.session_state.nav == 'Community':
    st.markdown("## 💬 Petizen Community")
    for p in posts:
        st.markdown(f"""
        <div class="app-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <span class="post-user">{p['user']}</span>
                <div style="display:flex; gap:8px;">
                    <span class="action-btn">+ Follow</span>
                    <span class="action-btn">+ Friend</span>
                </div>
            </div>
            <img src="{p['img']}" style="width:100%; border-radius:15px; margin-bottom:15px;">
            <p style="font-weight:500; color:#2D3436;">{p['text']}</p>
            <hr style="border:0.5px solid #F1F2F6; margin:15px 0;">
        """, unsafe_allow_html=True)
        for comm in p['comments']:
            st.markdown(f"<div class='comment-box'>{comm}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 4. BOTTOM NAV BAR
# ==========================================
st.markdown("<br><br><br>", unsafe_allow_html=True)
col_nav1, col_nav2, col_nav3 = st.columns(3)
with col_nav1:
    if st.button("🏠 Home"): st.session_state.nav = 'Home'; st.rerun()
with col_nav2:
    if st.button("🎟️ Deals"): st.session_state.nav = 'Deals'; st.rerun()
with col_nav3:
    if st.button("💬 Forum"): st.session_state.nav = 'Community'; st.rerun()

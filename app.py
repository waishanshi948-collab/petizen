import streamlit as st
import pandas as pd

# ==========================================
# 1. CSS STYLING (Aesthetic Mobile UI)
# ==========================================
st.set_page_config(page_title="Petizen", page_icon="🐾", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #FFF5F5 0%, #FFFFFF 100%);
    }
    .app-card {
        background-color: white;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.12);
        border: 1px solid #FFE3E3;
    }
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
    .shop-title { font-size: 22px; font-weight: bold; color: #2D3436; }
    .shop-tag { background: #FFF0F0; color: #FF6B6B; padding: 4px 10px; border-radius: 8px; font-size: 12px; margin-right: 5px; font-weight: 600; }
    .post-user { font-weight: bold; color: #FF6B6B; font-size: 16px; }
    .comment-box { background: #F8F9FA; padding: 12px; border-radius: 12px; margin-top: 8px; font-size: 14px; border-left: 3px solid #FF6B6B; }
    .action-btn { border: 1px solid #FF6B6B; background: white; color: #FF6B6B; border-radius: 15px; padding: 3px 12px; font-size: 12px; font-weight:bold; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. DATA (Using your Chinese Filenames)
# ==========================================

merchants = [
    {"id": 1, "name": "Fancy Tail Spa", "loc": "Central", "dist": 0.5, "price": 450, "rating": 4.9, "img": "商店1.jpg", "tel": "2345 1001", "serv": "Haircut, Bath, Aroma Spa"},
    {"id": 2, "name": "CityVet Clinic", "loc": "Wan Chai", "dist": 1.2, "price": 850, "rating": 4.8, "img": "商店2.jpg", "tel": "2345 1002", "serv": "Medical, Vaccine, Checkup"},
    {"id": 3, "name": "Paws Coffee", "loc": "Causeway Bay", "dist": 0.8, "price": 120, "rating": 4.7, "img": "商店3.jpg", "tel": "2345 1003", "serv": "Pet Afternoon Tea, Coffee"},
    {"id": 4, "name": "Splash Pool", "loc": "Sai Kung", "dist": 5.4, "price": 300, "rating": 4.6, "img": "商店4.jpg", "tel": "2345 1004", "serv": "Swimming, Grooming, Training"},
    {"id": 5, "name": "Royal Hotel", "loc": "Mid-Levels", "dist": 2.1, "price": 600, "rating": 5.0, "img": "商店5.jpg", "tel": "2345 1005", "serv": "24/7 Daycare, Boarding"},
    {"id": 6, "name": "Elite Groom", "loc": "Tsim Sha Tsui", "dist": 3.5, "price": 550, "rating": 4.7, "img": "商店6.jpg", "tel": "2345 1006", "serv": "Style Haircut, Nail Art"},
    {"id": 7, "name": "Pet Boutique", "loc": "Mong Kok", "dist": 4.2, "price": 200, "rating": 4.5, "img": "商店7.jpg", "tel": "2345 1007", "serv": "Designer Clothes, Toys"},
    {"id": 8, "name": "Gentle Vet", "loc": "Shatin", "dist": 6.8, "price": 750, "rating": 4.8, "img": "商店8.jpg", "tel": "2345 1008", "serv": "Clinic, Emergency Care"},
    {"id": 9, "name": "Bark Bakery", "loc": "Stanley", "dist": 7.2, "price": 150, "rating": 4.9, "img": "商店9.jpg", "tel": "2345 1009", "serv": "Baked Cakes, Snacks"},
    {"id": 10, "name": "Cloud Care", "loc": "Kowloon Tong", "dist": 3.0, "price": 400, "rating": 4.4, "img": "商店10.jpg", "tel": "2345 1010", "serv": "Interactive Play, Stay"},
    {"id": 11, "name": "Zen Retreat", "loc": "North Point", "dist": 2.5, "price": 80, "rating": 4.7, "img": "商店 11.jpg", "tel": "2345 1011", "serv": "Pet Massage, Pet Yoga"},
    {"id": 12, "name": "Uber Pet HK", "loc": "All HK", "dist": 0.1, "price": 180, "rating": 5.0, "img": "商店12.jpg", "tel": "2345 1012", "serv": "Transport, Pet Taxi"}
]

coupons = [
    {"name": "Bath + Haircut Bundle", "price": "$399", "orig": "$550"},
    {"name": "Cat Food Group Buy (x3)", "price": "$888", "orig": "$1200"},
    {"name": "Vaccine & Checkup Bundle", "price": "$699", "orig": "$950"},
    {"name": "Afternoon Tea for Two", "price": "$199", "orig": "$320"},
    {"name": "7-Day Stay Package", "price": "$2500", "orig": "$3500"},
    {"name": "Swimming Pass (10x)", "price": "$2200", "orig": "$3000"},
    {"name": "Puppy Starter Kit", "price": "$450", "orig": "$650"},
    {"name": "Grooming + Dental Bundle", "price": "$780", "orig": "$1100"},
    {"name": "Joint Spa Deal", "price": "$550", "orig": "$800"},
    {"name": "Obedience Training Bundle", "price": "$1500", "orig": "$2000"}
]

posts = [
    {"user": "@Meow_Mom", "img": "宠物1.jpg", "text": "My cute kitty climbed onto my bed today!", "comments": ["So cute!", "I want one too!"]},
    {"user": "@TinyCat", "img": "宠物2.jpg", "text": "My one-year-old cat is tiny enough to fit in a cup! So adorable.", "comments": ["Is it real?", "Too cute!"]},
    {"user": "@Bunny_Lover", "img": "宠物3.jpg", "text": "My bunny covered its eyes while I was changing! So polite.", "comments": ["What a gentleman!", "LOL!"]},
    {"user": "@Line_Pup", "img": "宠物4.jpg", "text": "My puppy looks exactly like the Line Friends dog character!", "comments": ["Twins!", "So lovely."]},
    {"user": "@Bird_Sir", "img": "宠物5.jpg", "text": "My little parrot's head is round like a gentleman.", "comments": ["Very elegant!", "Smart bird."]},
    {"user": "@Alpaca_Fan", "img": "宠物6.jpg", "text": "Every time I see my alpaca, I feel like riding it!", "comments": ["Don't! haha", "So fluffy."]},
    {"user": "@Piggy_Life", "img": "宠物7.jpg", "text": "Pet pigs are actually super cute too.", "comments": ["Oink oink!", "Adorable."]},
    {"user": "@Hedgehog_H", "img": "宠物8.jpg", "text": "The little hedgehog always messes around while I work.", "comments": ["Spiky helper!", "Busy guy."]}
]

# ==========================================
# 3. APP LOGIC
# ==========================================

if 'nav' not in st.session_state:
    st.session_state.nav = 'Passport'

# --- PAGE: PASSPORT ---
if st.session_state.nav == 'Passport':
    st.image("logo.jpg", width=100)
    st.markdown("# 🐾 Petizen Passport")
    with st.form("passport"):
        st.subheader("Pet Info")
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Pet Name *")
            st.text_input("Fur Color")
        with c2:
            st.text_input("Personality")
            st.text_input("Dietary Preference")
        st.subheader("Owner Info")
        owner_name = st.text_input("Owner Name *")
        owner_tel = st.text_input("Contact Number *")
        if st.form_submit_button("Enter Petizen"):
            if owner_name and owner_tel:
                st.session_state.user = owner_name
                st.session_state.nav = 'Home'
                st.rerun()

# --- PAGE: HOME (12 SHOPS & SORTING) ---
elif st.session_state.nav == 'Home':
    st.image("logo.jpg", width=70)
    st.markdown(f"### Hello, {st.session_state.user}! 👋")
    
    # Sorting logic
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
                <img src="{row['img']}" style="width:100%; border-radius:15px; margin-bottom:15px; height:180px; object-fit:cover;">
                <div style="display:flex; justify-content:space-between;">
                    <span class="shop-title">{row['name']}</span>
                    <span style="color:#FF6B6B; font-weight:bold;">⭐ {row['rating']}</span>
                </div>
                <div style="margin: 10px 0;">
                    <span class="shop-tag">📍 {row['loc']}</span>
                    <span class="shop-tag">💰 ${row['price']} up</span>
                </div>
                <p style="font-size:14px; color:#2D3436;"><b>Services:</b> {row['serv']}</p>
                <p style="font-size:12px; color:gray;">📞 Tel: {row['tel']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("Book Appointment", key=f"s_{idx}")

# --- PAGE: DEALS ---
elif st.session_state.nav == 'Deals':
    st.markdown("## 🎟️ Bundle Deals")
    for c in coupons:
        st.markdown(f"""
        <div class="app-card" style="border-left: 10px solid #FF6B6B;">
            <span style="font-weight:bold; font-size:18px;">{c['name']}</span><br>
            <span style="font-size:24px; font-weight:bold; color:#FF6B6B;">{c['price']}</span>
            <span style="text-decoration:line-through; color:#BDC3C7; font-size:14px;">{c['orig']}</span>
        </div>
        """, unsafe_allow_html=True)
        st.button("Claim Deal", key=f"d_{c['name']}")

# --- PAGE: COMMUNITY ---
elif st.session_state.nav == 'Community':
    st.markdown("## 💬 Petizen Community")
    for p in posts:
        st.markdown(f"""
        <div class="app-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="post-user">{p['user']}</span>
                <div><span class="action-btn">+ Follow</span> <span class="action-btn">+ Friend</span></div>
            </div>
            <img src="{p['img']}" style="width:100%; border-radius:15px; margin: 15px 0;">
            <p>{p['text']}</p>
        """, unsafe_allow_html=True)
        for comm in p['comments']:
            st.markdown(f"<div class='comment-box'>{comm}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- NAVIGATION ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🏠 Home"): st.session_state.nav = 'Home'; st.rerun()
with c2:
    if st.button("🎟️ Deals"): st.session_state.nav = 'Deals'; st.rerun()
with c3:
    if st.button("💬 Forum"): st.session_state.nav = 'Community'; st.rerun()

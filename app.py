import streamlit as st
import pandas as pd
import os

# ==========================================
# 1. HELPER: IMAGE MATCHER (For Chinese Filenames)
# ==========================================
def get_image_path(filename):
    try:
        files = os.listdir('.')
        for f in files:
            if f.strip() == filename.strip():
                return f
    except:
        pass
    return filename

# ==========================================
# 2. BEAUTIFUL CUSTOM CSS
# ==========================================
st.set_page_config(page_title="Petizen", page_icon="🐾", layout="centered")

st.markdown("""
    <style>
    /* Background & Font */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #FFF0F5 0%, #FFFFFF 50%, #F0F8FF 100%);
    }
    
    /* Sidebar Styling (Sticky Nav) */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #FFE4E1;
    }
    
    /* Rounded App Cards */
    .app-card {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 25px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(255, 182, 193, 0.2);
        border: 1px solid #FFE4E1;
    }
    
    /* Voucher Styling */
    .voucher-card {
        background: linear-gradient(90deg, #FFF9FA 0%, #FFF0F5 100%);
        border: 2px dashed #FFB6C1;
        border-radius: 20px;
        padding: 15px;
        margin-bottom: 15px;
    }

    /* Gradient Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #FF6B6B 0%, #FFB6C1 100%);
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        font-weight: bold;
        transition: 0.3s;
        width: 100%;
    }
    
    .shop-title { font-size: 22px; font-weight: 800; color: #4A4A4A; }
    .shop-tag { background: #FFF5F7; color: #FF6B6B; padding: 4px 10px; border-radius: 8px; font-size: 12px; margin-right: 5px; font-weight: bold; }
    .comment-bubble { background: #FDF2F4; padding: 10px; border-radius: 12px; margin-top: 8px; font-size: 13px; border-left: 4px solid #FFB6C1; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. INITIALIZE DATA & STATE
# ==========================================
if 'nav' not in st.session_state: st.session_state.nav = 'Home'
if 'comments_db' not in st.session_state: st.session_state.comments_db = {i: [] for i in range(8)}
if 'booking_shop_id' not in st.session_state: st.session_state.booking_shop_id = None

# --- DATABASE: MERCHANTS (12) ---
merchants = [
    {"id": 1, "name": "Fancy Tail Spa", "loc": "Central", "dist": 0.5, "price": 450, "rating": 4.9, "img": "商店1.jpg", "serv": "Haircut, Bath, Aroma Spa"},
    {"id": 2, "name": "CityVet Clinic", "loc": "Wan Chai", "dist": 1.2, "price": 850, "rating": 4.8, "img": "商店2.jpg", "serv": "Vaccine, Surgery"},
    {"id": 3, "name": "Paws Coffee", "loc": "Causeway Bay", "dist": 0.8, "price": 120, "rating": 4.7, "img": "商店3.jpg", "serv": "Pet Afternoon Tea"},
    {"id": 4, "name": "Splash Pool", "loc": "Sai Kung", "dist": 5.4, "price": 300, "rating": 4.6, "img": "商店4.jpg", "serv": "Swimming, Training"},
    {"id": 5, "name": "Royal Hotel", "loc": "Mid-Levels", "dist": 2.1, "price": 600, "rating": 5.0, "img": "商店5.jpg", "serv": "Boarding, Daycare"},
    {"id": 6, "name": "Elite Groom", "loc": "Tsim Sha Tsui", "dist": 3.5, "price": 550, "rating": 4.7, "img": "商店6.jpg", "serv": "Nail Art, Hair Dye"},
    {"id": 7, "name": "Pet Boutique", "loc": "Mong Kok", "dist": 4.2, "price": 200, "rating": 4.5, "img": "商店7.jpg", "serv": "Designer Clothes"},
    {"id": 8, "name": "Gentle Vet", "loc": "Shatin", "dist": 6.8, "price": 750, "rating": 4.8, "img": "商店8.jpg", "serv": "Clinic, Checkup"},
    {"id": 9, "name": "Bark Bakery", "loc": "Stanley", "dist": 7.2, "price": 150, "rating": 4.9, "img": "商店9.jpg", "serv": "Organic Cakes"},
    {"id": 10, "name": "Cloud Care", "loc": "Kowloon Tong", "dist": 3.0, "price": 400, "rating": 4.4, "img": "商店10.jpg", "serv": "Daycare"},
    {"id": 11, "name": "Zen Retreat", "loc": "North Point", "dist": 2.5, "price": 80, "rating": 4.7, "img": "商店 11.jpg", "serv": "Massage, Yoga"},
    {"id": 12, "name": "Pet Uber", "loc": "All HK", "dist": 0.1, "price": 180, "rating": 5.0, "img": "商店12.jpg", "serv": "Safe Taxi"}
]

# --- DATABASE: COUPONS (10+) ---
coupons = [
    {"n": "Summer Spa Bundle", "p": "$399", "o": "$550", "d": "Full Haircut + Milk Bath + Ear Clean"},
    {"n": "Cat Food Group Buy", "p": "$888", "o": "$1200", "d": "Bulk buy x3 bags of Premium Kibble"},
    {"n": "Vaccine Health Bundle", "p": "$650", "o": "$900", "d": "Rabies + DHPPi + Vet Checkup"},
    {"n": "Hotel Stay Bundle", "p": "$2400", "o": "$3200", "d": "7-Night Stay + 1 Free Spa Session"},
    {"n": "Doggy Swim Bundle", "p": "$1500", "o": "$2000", "d": "10-Lesson Entry Pass for Pool"},
    {"n": "Bakery Tea Combo", "p": "$150", "o": "$250", "d": "Cake + Drink + 1 Pet Snack"},
    {"n": "Puppy Training Pack", "p": "$1800", "o": "$2500", "d": "5 sessions of Obedience Training"},
    {"n": "Mega Grooming Deal", "p": "$999", "o": "$1500", "d": "3-session Haircut voucher"},
    {"n": "Dental & Ear Combo", "p": "$420", "o": "$600", "d": "Deep Cleaning for healthy pets"},
    {"n": "Friend Referral Deal", "p": "$500", "o": "$800", "d": "Two pets groom together and save!"}
]

# --- DATABASE: FORUM (8) ---
posts = [
    {"id": 0, "user": "@Kitty_Mom", "img": "宠物1.jpg", "text": "My kitty climbed onto my bed today! So soft."},
    {"id": 1, "user": "@TinyPaw", "img": "宠物2.jpg", "text": "Tiny enough to fit in a cup! So adorable."},
    {"id": 2, "user": "@Bunny_Fan", "img": "宠物3.jpg", "text": "Polite bunny covered its eyes while I was changing!"},
    {"id": 3, "user": "@LineFriends", "img": "宠物4.jpg", "text": "Puppy looks exactly like the character!"},
    {"id": 4, "user": "@Bird_Sir", "img": "宠物5.jpg", "text": "Parrot head is round like a true gentleman."},
    {"id": 5, "user": "@Alpaca_Lo", "img": "宠物6.jpg", "text": "The fluff is irresistible!"},
    {"id": 6, "user": "@Piggy_Life", "img": "宠物7.jpg", "text": "Pigs are super cute pets too."},
    {"id": 7, "user": "@Hedgehog_H", "img": "宠物8.jpg", "text": "Spiky coworker messes with my laptop!"}
]

# ==========================================
# 4. STICKY SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.image("logo.jpg", width=100)
    st.markdown("### Menu")
    if st.button("🏠 Home (Shops)"): st.session_state.nav = 'Home'; st.rerun()
    if st.button("🎟️ Deals (Coupons)"): st.session_state.nav = 'Deals'; st.rerun()
    if st.button("💬 Community (Forum)"): st.session_state.nav = 'Community'; st.rerun()
    st.markdown("---")
    st.write("Logged in as:")
    st.info(st.session_state.get('user', 'Guest'))

# ==========================================
# 5. PAGE CONTENT
# ==========================================

# --- PAGE: HOME (SHOPS & BOOKING) ---
if st.session_state.nav == 'Home':
    # Initial Passport Check
    if 'user' not in st.session_state:
        st.markdown("# 🐾 Welcome to Petizen")
        with st.form("passport"):
            name = st.text_input("Owner Name *")
            st.text_input("Pet Name")
            if st.form_submit_button("Enter App"):
                if name: st.session_state.user = name; st.rerun()
    else:
        st.markdown(f"## Petizen Services ✨")
        sort_option = st.selectbox("Sort By:", ["Distance (Nearest)", "Rating (Highest)", "Price (Low-High)", "Price (High-Low)"])
        df = pd.DataFrame(merchants)
        if "Distance" in sort_option: df = df.sort_values("dist")
        elif "Rating" in sort_option: df = df.sort_values("rating", ascending=False)
        elif "Low-High" in sort_option: df = df.sort_values("price")
        else: df = df.sort_values("price", ascending=False)

        for idx, row in df.iterrows():
            img = get_image_path(row['img'])
            with st.container():
                st.markdown(f"""<div class="app-card">
                    <span class="shop-title">{row['name']}</span> <span style="color:#FF6B6B;">⭐ {row['rating']}</span>""", unsafe_allow_html=True)
                st.image(img, use_column_width=True)
                st.markdown(f"""<div style="margin: 10px 0;"><span class="shop-tag">📍 {row['loc']}</span><span class="shop-tag">💰 ${row['price']}</span></div>
                    <p style="color:#555; font-size:14px;"><b>Services:</b> {row['serv']}</p></div>""", unsafe_allow_html=True)
                if st.button(f"Book Appointment @ {row['name']}", key=f"bk_{idx}"):
                    st.session_state.booking_shop_id = row['id']
                if st.session_state.booking_shop_id == row['id']:
                    slot = st.selectbox("Pick a Time Slot:", ["1PM - 2PM", "2PM - 3PM", "3PM - 4PM", "4PM - 5PM"], key=f"s_{idx}")
                    if st.button("Confirm Reservation", key=f"cf_{idx}"):
                        st.success(f"Success! {slot} booked."); st.session_state.booking_shop_id = None

# --- PAGE: DEALS (10+ COUPONS) ---
elif st.session_state.nav == 'Deals':
    st.markdown("## 🎟️ Exclusive Bundle Deals")
    st.write("Group-buy vouchers and bundled services for extra savings.")
    for idx, c in enumerate(coupons):
        st.markdown(f"""<div class="voucher-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:bold; font-size:18px; color:#4A4A4A;">{c['n']}</span>
                <span style="background:#FF6B6B; color:white; padding:2px 10px; border-radius:10px; font-size:11px;">PROMO</span>
            </div>
            <p style="color:gray; font-size:13px; margin:5px 0;">{c['d']}</p>
            <span style="font-size:24px; font-weight:800; color:#FF6B6B;">{c['p']}</span>
            <span style="text-decoration:line-through; color:#BDC3C7; font-size:15px; margin-left:10px;">{c['o']}</span>
            </div>""", unsafe_allow_html=True)
        if st.button(f"Claim Voucher: {c['n']}", key=f"v_{idx}"): st.toast("Voucher saved to wallet!")

# --- PAGE: COMMUNITY (FORUM & COMMENTS) ---
elif st.session_state.nav == 'Community':
    st.markdown("## 💬 Forum Feed")
    for p in posts:
        pet_img = get_image_path(p['img'])
        with st.container():
            st.markdown(f"""<div class="app-card"><div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                    <span style="font-weight:bold; color:#FF6B6B;">{p['user']}</span><div>""", unsafe_allow_html=True)
            if st.button("+ Follow", key=f"f_{p['id']}"): st.toast("Followed!")
            if st.button("+ Friend", key=f"fr_{p['id']}"): st.toast("Requested!")
            st.markdown("</div></div>", unsafe_allow_html=True)
            st.image(pet_img, use_column_width=True)
            st.markdown(f"<b>{p['text']}</b><hr>", unsafe_allow_html=True)
            for c in st.session_state.comments_db[p['id']]:
                st.markdown(f"<div class='comment-bubble'>🗨️ {c}</div>", unsafe_allow_html=True)
            nc = st.text_input("Add a comment...", key=f"i_{p['id']}")
            if st.button("Post", key=f"p_{p['id']}"):
                if nc: st.session_state.comments_db[p['id']].append(nc); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

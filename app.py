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
# 2. BEAUTIFUL CUSTOM CSS (Aesthetic Upgrade)
# ==========================================
st.set_page_config(page_title="Petizen", page_icon="🐾", layout="centered")

st.markdown("""
    <style>
    /* Bubbly Pastel Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #FFF0F5 0%, #FFFFFF 50%, #F0F8FF 100%);
    }
    
    /* Cute Rounded Cards */
    .app-card {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 30px;
        padding: 25px;
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(255, 182, 193, 0.2);
        border: 2px solid #FFE4E1;
    }
    
    /* Gradient Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #FF6B6B 0%, #FFB6C1 100%);
        color: white !important;
        border-radius: 30px !important;
        border: none !important;
        font-weight: bold;
        transition: 0.3s ease;
        height: 50px;
        width: 100%;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
    }

    /* Small Interaction Buttons */
    .action-btn {
        background: #FFF0F5;
        border: 1.5px solid #FF6B6B;
        color: #FF6B6B;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: bold;
        cursor: pointer;
        display: inline-block;
        margin-right: 5px;
    }

    /* Typography */
    .shop-title { font-size: 24px; font-weight: 800; color: #4A4A4A; }
    .shop-tag { background: #FFF5F7; color: #FF6B6B; padding: 5px 12px; border-radius: 10px; font-size: 13px; margin-right: 5px; font-weight: bold; }
    .comment-bubble { background: #FDF2F4; padding: 12px; border-radius: 15px; margin-top: 10px; font-size: 14px; color: #555; border-left: 4px solid #FFB6C1; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. INITIALIZE SESSION STATE
# ==========================================
if 'nav' not in st.session_state: st.session_state.nav = 'Passport'
if 'comments_db' not in st.session_state:
    st.session_state.comments_db = {i: [] for i in range(8)} # 8 Posts
if 'friends' not in st.session_state: st.session_state.friends = set()
if 'following' not in st.session_state: st.session_state.following = set()
if 'booking_shop_id' not in st.session_state: st.session_state.booking_shop_id = None

# ==========================================
# 4. DATABASE (Chinese Filenames)
# ==========================================
merchants = [
    {"id": 1, "name": "Fancy Tail Spa", "loc": "Central", "dist": 0.5, "price": 450, "rating": 4.9, "img": "商店1.jpg", "tel": "2345 1001", "serv": "Styling, Aroma Bath"},
    {"id": 2, "name": "CityVet Clinic", "loc": "Wan Chai", "dist": 1.2, "price": 850, "rating": 4.8, "img": "商店2.jpg", "tel": "2345 1002", "serv": "Vaccine, Surgery"},
    {"id": 3, "name": "Paws Coffee", "loc": "Causeway Bay", "dist": 0.8, "price": 120, "rating": 4.7, "img": "商店3.jpg", "tel": "2345 1003", "serv": "Afternoon Tea, Social"},
    {"id": 4, "name": "Splash Pool", "loc": "Sai Kung", "dist": 5.4, "price": 300, "rating": 4.6, "img": "商店4.jpg", "tel": "2345 1004", "serv": "Swimming, Training"},
    {"id": 5, "name": "Royal Hotel", "loc": "Mid-Levels", "dist": 2.1, "price": 600, "rating": 5.0, "img": "商店5.jpg", "tel": "2345 1005", "serv": "Boarding, Daycare"},
    {"id": 6, "name": "Elite Groom", "loc": "Tsim Sha Tsui", "dist": 3.5, "price": 550, "rating": 4.7, "img": "商店6.jpg", "tel": "2345 1006", "serv": "Nail Art, Hair Dye"},
    {"id": 7, "name": "Pet Boutique", "loc": "Mong Kok", "dist": 4.2, "price": 200, "rating": 4.5, "img": "商店7.jpg", "tel": "2345 1007", "serv": "Clothes, Toys"},
    {"id": 8, "name": "Gentle Vet", "loc": "Shatin", "dist": 6.8, "price": 750, "rating": 4.8, "img": "商店8.jpg", "tel": "2345 1008", "serv": "Emergency, Dental"},
    {"id": 9, "name": "Bark Bakery", "loc": "Stanley", "dist": 7.2, "price": 150, "rating": 4.9, "img": "商店9.jpg", "tel": "2345 1009", "serv": "Organic Cakes, Treats"},
    {"id": 10, "name": "Cloud Care", "loc": "Kowloon Tong", "dist": 3.0, "price": 400, "rating": 4.4, "img": "商店10.jpg", "tel": "2345 1010", "serv": "Daycare, Playtime"},
    {"id": 11, "name": "Zen Retreat", "loc": "North Point", "dist": 2.5, "price": 80, "rating": 4.7, "img": "商店 11.jpg", "tel": "2345 1011", "serv": "Massage, Pet Yoga"},
    {"id": 12, "name": "Pet Uber", "loc": "All Districts", "dist": 0.1, "price": 180, "rating": 5.0, "img": "商店12.jpg", "tel": "2345 1012", "serv": "Safe Transport"}
]

posts = [
    {"id": 0, "user": "@Kitty_Mom", "img": "宠物1.jpg", "text": "My cute kitty climbed onto my bed today! So soft."},
    {"id": 1, "user": "@TinyPaw", "img": "宠物2.jpg", "text": "My one-year-old cat fits in a cup! So adorable."},
    {"id": 2, "user": "@Bunny_Fan", "img": "宠物3.jpg", "text": "Bunny covered its eyes while I was changing! Polite boy."},
    {"id": 3, "user": "@LineFriends", "img": "宠物4.jpg", "text": "My puppy looks exactly like the Line Friends character!"},
    {"id": 4, "user": "@Bird_Sir", "img": "宠物5.jpg", "text": "Parrot head is round like a gentleman."},
    {"id": 5, "user": "@Alpaca_Lo", "img": "宠物6.jpg", "text": "Urge to ride my fluffy alpaca is too strong!"},
    {"id": 6, "user": "@Piggy_Life", "img": "宠物7.jpg", "text": "Pet pigs are actually super cute too."},
    {"id": 7, "user": "@Hedgehog_H", "img": "宠物8.jpg", "text": "Hedgehog messes around while I work!"}
]

# ==========================================
# 5. PAGE ROUTING
# ==========================================

# --- PAGE: PASSPORT ---
if st.session_state.nav == 'Passport':
    st.image("logo.jpg", width=120)
    st.markdown("<h1 style='color:#FF6B6B;'>🐾 Create Passport</h1>", unsafe_allow_html=True)
    with st.form("passport"):
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Pet Name")
            st.text_input("Fur Color")
        with c2:
            st.text_input("Personality")
            st.text_input("Diet Preference")
        owner_name = st.text_input("Owner Name")
        owner_tel = st.text_input("Contact Phone")
        if st.form_submit_button("Enter Petizen World"):
            if owner_name:
                st.session_state.user = owner_name
                st.session_state.nav = 'Home'
                st.rerun()

# --- PAGE: HOME (SHOPPING & BOOKING) ---
elif st.session_state.nav == 'Home':
    st.image("logo.jpg", width=80)
    st.markdown(f"## Hi {st.session_state.user}! ✨")
    
    sort_option = st.selectbox("Sort By:", ["Distance (Nearest)", "Rating (Highest)", "Price (Low to High)", "Price (High to Low)"])
    df = pd.DataFrame(merchants)
    if "Distance" in sort_option: df = df.sort_values("dist")
    elif "Rating" in sort_option: df = df.sort_values("rating", ascending=False)
    elif "Low to High" in sort_option: df = df.sort_values("price")
    else: df = df.sort_values("price", ascending=False)

    for idx, row in df.iterrows():
        img_path = get_image_path(row['img'])
        with st.container():
            st.markdown(f"""<div class="app-card">
                <span class="shop-title">{row['name']}</span> <span style="color:#FF6B6B;">⭐ {row['rating']}</span>""", unsafe_allow_html=True)
            st.image(img_path, use_column_width=True)
            st.markdown(f"""<div style="margin: 10px 0;"><span class="shop-tag">📍 {row['loc']}</span><span class="shop-tag">💰 ${row['price']}</span></div>
                <p style="color:#555;"><b>Services:</b> {row['serv']}<br>📞 Tel: {row['tel']}</p></div>""", unsafe_allow_html=True)
            
            # Booking Logic
            if st.button(f"Book at {row['name']}", key=f"bk_{idx}"):
                st.session_state.booking_shop_id = row['id']
            
            if st.session_state.booking_shop_id == row['id']:
                slot = st.selectbox("Select Time Slot:", ["1:00 PM - 2:00 PM", "2:00 PM - 3:00 PM", "3:00 PM - 4:00 PM", "4:00 PM - 5:00 PM"], key=f"slot_{idx}")
                if st.button("Confirm Booking", key=f"conf_{idx}"):
                    st.success(f"✅ Success! Reserved for {slot}")
                    st.session_state.booking_shop_id = None

# --- PAGE: COMMUNITY (FORUM & COMMENTS) ---
elif st.session_state.nav == 'Community':
    st.markdown("## 💬 Forum Feed")
    for p in posts:
        pet_img = get_image_path(p['img'])
        with st.container():
            st.markdown(f"""<div class="app-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                    <span class="post-user">{p['user']}</span><div>""", unsafe_allow_html=True)
            
            # Follow/Friend logic
            if st.button(f"+ Follow", key=f"foll_{p['id']}"): st.toast(f"Followed {p['user']}!")
            if st.button(f"+ Friend", key=f"fri_{p['id']}"): st.toast(f"Friend Request Sent to {p['user']}!")
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            st.image(pet_img, use_column_width=True)
            st.markdown(f"<b>{p['text']}</b><hr>", unsafe_allow_html=True)
            
            # Real Comments
            for c in st.session_state.comments_db[p['id']]:
                st.markdown(f"<div class='comment-bubble'>🗨️ {c}</div>", unsafe_allow_html=True)
            
            new_c = st.text_input("Write a comment...", key=f"input_{p['id']}")
            if st.button("Post", key=f"post_{p['id']}"):
                if new_c:
                    st.session_state.comments_db[p['id']].append(new_c)
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# --- NAVIGATION BAR ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🏠 Home"): st.session_state.nav = 'Home'; st.rerun()
with c2:
    if st.button("🎟️ Deals"): st.session_state.nav = 'Deals'; st.rerun() # Deals page kept from previous
with c3:
    if st.button("💬 Forum"): st.session_state.nav = 'Community'; st.rerun()

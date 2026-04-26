import streamlit as st
import pandas as pd
import os
import time

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
# 2. BEAUTIFUL CUSTOM CSS (Including Passport & Virtual Pet)
# ==========================================
st.set_page_config(page_title="Petizen", page_icon="🐾", layout="centered")

st.markdown("""
    <style>
    /* Background & Global Font */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #FFF0F5 0%, #FFFFFF 50%, #F0F8FF 100%);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #FFE4E1;
    }
    
    /* Rounded App Cards */
    .app-card {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 25px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(255, 182, 193, 0.2);
        border: 1px solid #FFE4E1;
    }
    
    /* Passport Specific Cards */
    .passport-card {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #F1F2F6;
    }
    .status-green { background: #E8F8F5; color: #2ECC71; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: bold; }
    .check-item { color: #2ECC71; font-size: 14px; margin-right: 10px; }
    
    /* Virtual Pet Widget */
    .virtual-pet-box {
        background: linear-gradient(90deg, #FFF5F7 0%, #FFFFFF 100%);
        border-radius: 25px;
        padding: 15px;
        text-align: center;
        border: 2px dashed #FFB6C1;
        margin-bottom: 25px;
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.15);
    }
    .cat-emoji { font-size: 65px; line-height: 1; }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #FF6B6B 0%, #FFB6C1 100%);
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        font-weight: bold;
        transition: 0.3s;
        width: 100%;
    }
    .share-btn>button { background: #FF4757 !important; }

    .stTextInput>div>div>input, .stSelectbox>div>div>div { border-radius: 20px !important; border: 1px solid #FFB6C1 !important; }
    .shop-title { font-size: 22px; font-weight: 800; color: #4A4A4A; }
    .shop-tag { background: #FFF5F7; color: #FF6B6B; padding: 4px 10px; border-radius: 8px; font-size: 12px; margin-right: 5px; font-weight: bold; }
    .comment-bubble { background: #FDF2F4; padding: 10px; border-radius: 12px; margin-top: 8px; font-size: 13px; border-left: 4px solid #FFB6C1; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. INITIALIZE DATA & SESSION STATE
# ==========================================
if 'nav' not in st.session_state: st.session_state.nav = 'Form'
if 'comments_db' not in st.session_state: st.session_state.comments_db = {i: [] for i in range(8)}
if 'booking_shop_id' not in st.session_state: st.session_state.booking_shop_id = None
if 'happiness' not in st.session_state: st.session_state.happiness = 0
if 'smile_trigger' not in st.session_state: st.session_state.smile_trigger = False

# --- DATABASES (Keeping exact Chinese names for images) ---
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

coupons = [
    {"n": "Summer Spa Bundle", "p": "$399", "o": "$550", "d": "Full Grooming + Aroma Bath"},
    {"n": "Cat Food Group Buy", "p": "$888", "o": "$1200", "d": "3 Bags Premium Kibble"},
    {"n": "Vaccine Health Bundle", "p": "$650", "o": "$900", "d": "Rabies + DHPPi + Checkup"},
    {"n": "Hotel Stay Bundle", "p": "$2400", "o": "$3200", "d": "7-Night Stay + 1 Spa"},
    {"n": "Doggy Swim Pass", "p": "$1500", "o": "$2000", "d": "10-Lesson Pool Pass"},
    {"n": "Bakery Tea Combo", "p": "$150", "o": "$250", "d": "Cake + Drink + Snack"},
    {"n": "Puppy Training Pack", "p": "$1800", "o": "$2500", "d": "5 sessions of Training"},
    {"n": "Mega Grooming Deal", "p": "$999", "o": "$1500", "d": "3 Haircut Voucher"},
    {"n": "Dental & Ear Combo", "p": "$420", "o": "$600", "d": "Professional Deep Clean"},
    {"n": "Friend Referral Deal", "p": "$500", "o": "$800", "d": "2 Pets Save Together!"}
]

posts = [
    {"id": 0, "user": "@Kitty_Mom", "img": "宠物1.jpg", "text": "My kitty climbed onto my bed today!"},
    {"id": 1, "user": "@TinyPaw", "img": "宠物2.jpg", "text": "Tiny enough to fit in a cup!"},
    {"id": 2, "user": "@Bunny_Fan", "img": "宠物3.jpg", "text": "Polite bunny covered its eyes!"},
    {"id": 3, "user": "@LineFriends", "img": "宠物4.jpg", "text": "Puppy looks exactly like the character!"},
    {"id": 4, "user": "@Bird_Sir", "img": "宠物5.jpg", "text": "Parrot head is round like a gentleman."},
    {"id": 5, "user": "@Alpaca_Lo", "img": "宠物6.jpg", "text": "Fluffy Alpaca day!"},
    {"id": 6, "user": "@Piggy_Life", "img": "宠物7.jpg", "text": "Pigs are cute pets too."},
    {"id": 7, "user": "@Hedgehog_H", "img": "宠物8.jpg", "text": "Work from home with a hedgehog!"}
]

# --- VIRTUAL PET COMPONENT ---
def render_virtual_pet():
    if st.session_state.smile_trigger:
        cat_face = "😻"
        msg = "YAY! Happiness +1 💖"
        # Reset trigger so it goes back to normal next action
        st.session_state.smile_trigger = False 
    else:
        cat_face = "😺"
        msg = "Hi! Let's book something fun!"

    st.markdown(f"""
    <div class="virtual-pet-box">
        <div class="cat-emoji">{cat_face}</div>
        <h4 style="color:#FF6B6B; margin:5px 0;">{msg}</h4>
        <p style="color:gray; font-size:14px; margin:0;">Total Happiness Level: <b>{st.session_state.happiness}</b> 🌟</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 4. STICKY SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.image(get_image_path("logo.jpg"), width=120)
    st.markdown("### Nav Menu")
    
    # Check if user is logged in to show full menu
    if 'user' in st.session_state:
        if st.button("🛂 My Passport"): st.session_state.nav = 'Passport_Display'; st.rerun()
        if st.button("🏠 Home (Shops)"): st.session_state.nav = 'Home'; st.rerun()
        if st.button("🎟️ Deals (Coupons)"): st.session_state.nav = 'Deals'; st.rerun()
        if st.button("💬 Community"): st.session_state.nav = 'Community'; st.rerun()
        st.markdown("---")
        st.write("Welcome,")
        st.info(st.session_state.user['owner_name'])
        st.write(f"Pet: {st.session_state.user['pet_name']}")
    else:
        st.warning("Please create your Passport first.")

# ==========================================
# 5. PAGE CONTENT
# ==========================================

# --- PAGE 1: FORM (ONBOARDING) ---
if st.session_state.nav == 'Form':
    if 'user' not in st.session_state:
        st.markdown("# 🐾 Create Pet Passport")
        st.write("Complete your profile to unlock Petizen!")
        with st.form("passport_form"):
            c1, c2 = st.columns(2)
            with c1:
                p_name = st.text_input("Pet Name *")
                p_species = st.selectbox("Species *", ["Cat", "Dog", "Bird", "Bunny", "Other"])
                p_color = st.text_input("Fur Color")
                p_gender = st.radio("Gender", ["Boy", "Girl"])
            with c2:
                p_age = st.text_input("Age (e.g., 2 years)")
                p_diet = st.text_input("Dietary Habits")
                p_vaccine = st.radio("Vaccinated?", ["Yes", "No"])
            
            st.markdown("---")
            o_name = st.text_input("Owner Name *")
            o_tel = st.text_input("Owner Contact Number *")
            
            if st.form_submit_button("Generate Passport"):
                if p_name and o_name and o_tel:
                    st.session_state.user = {
                        "pet_name": p_name, "species": p_species, "color": p_color, 
                        "gender": p_gender, "diet": p_diet, "vaccine": p_vaccine, 
                        "owner_name": o_name, "tel": o_tel, "age": p_age
                    }
                    st.session_state.nav = 'Passport_Display' # Redirect to display page!
                    st.rerun()
                else:
                    st.error("Please fill in the required fields (*).")

# --- PAGE 2: PASSPORT DISPLAY (AESTHETIC UI) ---
elif st.session_state.nav == 'Passport_Display':
    u = st.session_state.user
    st.markdown("<h2 style='text-align: center;'>Pet Passport</h2>", unsafe_allow_html=True)
    
    # 1. Profile Header Card
    st.markdown("<div class='passport-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.5])
    with col1:
        # Load cat.jpg exactly as requested
        st.image(get_image_path("cat.jpg"), use_column_width=True)
    with col2:
        st.markdown(f"<h1 style='color:#2D3436; margin-bottom:5px;'>{u['pet_name']} ❤️</h1>", unsafe_allow_html=True)
        st.markdown(f"🐾 **Breed/Species:** {u['color']} {u['species']}<br>📅 **Age:** {u['age'] if u['age'] else 'Secret'}<br>👤 **Owner:** {u['owner_name']}", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. Vaccination Status
    st.markdown(f"""
    <div class='passport-card'>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <h4 style='margin:0;'>🛡️ Vaccination Status</h4>
            <span class='status-green'>{'Up to date' if u['vaccine']=='Yes' else 'Pending'}</span>
        </div>
        <p style='color:gray; font-size:13px;'>All core vaccines verified.</p>
        <div>
            <span class='check-item'>✔️ Rabies</span>
            <span class='check-item'>✔️ DHPP</span>
            <span class='check-item'>✔️ Bordetella</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Medical & QR
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
        <div class='passport-card' style='height: 180px;'>
            <h4 style='margin:0;'>🏥 Medical History</h4>
            <ul style='font-size:13px; color:gray; padding-left:15px; margin-top:10px;'>
                <li>Wellness checkup - Apr 2024</li>
                <li>Microchipped - Jan 2023</li>
                <li>No known allergies.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class='passport-card' style='height: 180px; text-align:center;'>
            <h4 style='margin:0;'>🆔 QR Code</h4>
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=PetizenVerified" style="width:90px; margin-top:10px;">
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='share-btn'>", unsafe_allow_html=True)
    if st.button("🔗 Share with Vet / Services"):
        st.success("Passport link copied!")
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 3: HOME (SHOPS & BOOKING & VIRTUAL PET) ---
elif st.session_state.nav == 'Home':
    render_virtual_pet() # Add virtual cat here
    
    st.markdown(f"## Explore Services ✨")
    search_query = st.text_input("🔍 Search for services (Grooming, Vet, Pool, etc.)...").lower()
    sort_option = st.selectbox("Sort By:", ["Distance (Nearest)", "Rating (Highest)", "Price (Low-High)", "Price (High-Low)"])
    
    df = pd.DataFrame(merchants)
    if search_query:
        df = df[df['serv'].str.lower().contains(search_query) | df['name'].str.lower().contains(search_query)]
    
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
                slot = st.selectbox("Select Time Slot:", ["1PM-2PM", "2PM-3PM", "3PM-4PM", "4PM-5PM"], key=f"s_{idx}")
                if st.button("Confirm Reservation", key=f"cf_{idx}"):
                    # Trigger Happiness and Animation!
                    st.session_state.happiness += 1
                    st.session_state.smile_trigger = True
                    st.session_state.booking_shop_id = None
                    st.balloons()
                    st.rerun()

# --- PAGE 4: DEALS (COUPONS & VIRTUAL PET) ---
elif st.session_state.nav == 'Deals':
    render_virtual_pet() # Add virtual cat here
    
    st.markdown("## 🎟️ Exclusive Bundle Deals")
    for idx, c in enumerate(coupons):
        st.markdown(f"""<div class="voucher-card">
            <span style="font-weight:bold; font-size:18px;">{c['n']}</span>
            <p style="color:gray; font-size:13px; margin:5px 0;">{c['d']}</p>
            <span style="font-size:24px; font-weight:800; color:#FF6B6B;">{c['p']}</span>
            <span style="text-decoration:line-through; color:#BDC3C7; font-size:15px; margin-left:10px;">{c['o']}</span>
            </div>""", unsafe_allow_html=True)
        if st.button(f"Claim Voucher: {c['n']}", key=f"v_{idx}"): 
            # Trigger Happiness!
            st.session_state.happiness += 1
            st.session_state.smile_trigger = True
            st.toast("Voucher Saved!")
            st.rerun()

# --- PAGE 5: COMMUNITY (FORUM) ---
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
            
            nc = st.text_input("Write a comment...", key=f"i_{p['id']}")
            if st.button("Post Comment", key=f"p_{p['id']}"):
                if nc: 
                    st.session_state.comments_db[p['id']].append(nc)
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

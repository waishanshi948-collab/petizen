import streamlit as st
import pandas as pd

# ==========================================
# 1. PAGE CONFIGURATION & AESTHETICS (CSS)
# ==========================================
st.set_page_config(page_title="Petizen", page_icon="🐾", layout="centered")

st.markdown("""
    <style>
    /* Main Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #FFF5F5 0%, #FFFFFF 100%);
    }
    
    /* Card UI Design */
    .app-card {
        background-color: white;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.12);
        border: 1px solid #FFE3E3;
    }
    
    /* Button Styling (Petizen Pink) */
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
    
    /* Shop Detail Styling */
    .shop-title { font-size: 22px; font-weight: bold; color: #2D3436; }
    .shop-tag { background: #FFF0F0; color: #FF6B6B; padding: 4px 10px; border-radius: 8px; font-size: 12px; margin-right: 5px; font-weight: 600; }
    
    /* Social Media Post Styling */
    .post-user { font-weight: bold; color: #FF6B6B; font-size: 16px; }
    .comment-box { background: #F8F9FA; padding: 12px; border-radius: 12px; margin-top: 8px; font-size: 14px; border-left: 3px solid #FF6B6B; }
    .follow-btn { border: 1px solid #FF6B6B; background: white; color: #FF6B6B; border-radius: 15px; padding: 3px 12px; font-size: 12px; cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. DATA PREPARATION (ENGLISH)
# ==========================================

# 12 Merchants with Detailed Services
merchants = [
    {"id": 1, "name": "Fancy Tail Spa", "loc": "Central", "dist": 0.5, "price": 450, "rating": 4.9, "img": "商店1.jpg", "tel": "+852 2345 1001", "serv": "Professional Haircut, Milk Bath, Aroma Spa Therapy"},
    {"id": 2, "name": "CityVet Health Center", "loc": "Wan Chai", "dist": 1.2, "price": 800, "rating": 4.8, "img": "商店2.jpg", "tel": "+852 2345 1002", "serv": "General Checkup, Vaccinations, Surgery, Dental Care"},
    {"id": 3, "name": "Paws & Chill Cafe", "loc": "Causeway Bay", "dist": 0.8, "price": 120, "rating": 4.7, "img": "商店3.jpg", "tel": "+852 2345 1003", "serv": "Pet Afternoon Tea, Organic Snacks, Owner-Pet Coffee Social"},
    {"id": 4, "name": "Summer Splash Pool", "loc": "Sai Kung", "dist": 5.4, "price": 300, "rating": 4.6, "img": "商店4.jpg", "tel": "+852 2345 1004", "serv": "Indoor Heated Swimming, Life Jacket Rental, Drying Service"},
    {"id": 5, "name": "Royal Paw Hotel", "loc": "Mid-Levels", "dist": 2.1, "price": 600, "rating": 5.0, "img": "商店5.jpg", "tel": "+852 2345 1005", "serv": "Luxury Boarding, 24/7 CCTV Access, Daily Walking Service"},
    {"id": 6, "name": "Elite Grooming Studio", "loc": "Tsim Sha Tsui", "dist": 3.5, "price": 550, "rating": 4.7, "img": "商店6.jpg", "tel": "+852 2345 1006", "serv": "Show-level Grooming, Paw Pedicure, Fur Coloring"},
    {"id": 7, "name": "Pet Boutique Fashion", "loc": "Mong Kok", "dist": 4.2, "price": 200, "rating": 4.5, "img": "商店7.jpg", "tel": "+852 2345 1007", "serv": "Designer Clothes, Custom Collars, Seasonal Accessories"},
    {"id": 8, "name": "Gentle Vet Clinic", "loc": "Shatin", "dist": 6.8, "price": 750, "rating": 4.8, "img": "商店8.jpg", "tel": "+852 2345 1008", "serv": "Emergency Care, Microchipping, Internal Medicine"},
    {"id": 9, "name": "Bark & Bakery", "loc": "Stanley", "dist": 7.2, "price": 150, "rating": 4.9, "img": "商店9.jpg", "tel": "+852 2345 1009", "serv": "Freshly Baked Pet Cakes, Birthday Party Hosting"},
    {"id": 10, "name": "Cloud Daycare", "loc": "Kowloon Tong", "dist": 3.0, "price": 400, "rating": 4.4, "img": "商店10.jpg", "tel": "+852 2345 1010", "serv": "Interactive Play Groups, Basic Obedience Training"},
    {"id": 11, "name": "Zen Pet Retreat", "loc": "North Point", "dist": 2.5, "price": 80, "rating": 4.7, "img": "商店 11.jpg", "tel": "+852 2345 1011", "serv": "Pet Massage, Meditation Music Therapy, Quiet Stay"},
    {"id": 12, "name": "Luxury Pet Uber", "loc": "All Districts", "dist": 0.1, "price": 150, "rating": 5.0, "img": "商店12.jpg", "tel": "+852 2345 1012", "serv": "Point-to-Point Transport, Pet Safety Seats, Large Breed Friendly"}
]

# 10 Group-Buy Coupons
coupons = [
    {"name": "Bundle: Bath + Grooming", "price": "$399", "orig": "$550", "desc": "Full set service for small/medium pets."},
    {"name": "Group Buy: Premium Food (3 Bags)", "price": "$888", "orig": "$1200", "desc": "Mix & Match flavors available."},
    {"name": "Annual Vaccine + Checkup", "price": "$699", "orig": "$950", "desc": "Comprehensive health guarantee."},
    {"name": "Pet Afternoon Tea for Two", "price": "$199", "orig": "$320", "desc": "Includes 2 drinks and 2 pet snacks."},
    {"name": "7-Day Luxury Boarding Pass", "price": "$3500", "orig": "$4500", "desc": "Free spa included on the last day."},
    {"name": "Swimming Pass (10 Entries)", "price": "$2200", "orig": "$3000", "desc": "Valid for 12 months, all sizes."},
    {"name": "Puppy Starter Bundle", "price": "$450", "orig": "$700", "desc": "Toys, bowls, and first grooming."},
    {"name": "Emergency Care Prepaid Card", "price": "$1000", "orig": "$1300", "desc": "Instant credit for any clinic service."},
    {"name": "Bestie Discount (2 Pets)", "price": "$600", "orig": "$900", "desc": "Book together and save 30% on spa."},
    {"name": "VIP Dental & Ear Cleaning", "price": "$480", "orig": "$650", "desc": "Deep cleaning by professionals."}
]

# 8 Forum Posts with Translated Stories
posts = [
    {"user": "@Kitty_Lover", "img": "宠物1.jpg", "text": "My cute kitty climbed onto my bed today! So soft.", "comments": ["So cute!", "My heart is melting!"]},
    {"user": "@TinyPaw_Mom", "img": "宠物2.jpg", "text": "My one-year-old cat is tiny enough to fit in a cup! So adorable.", "comments": ["Wait, how is that possible?", "A cup of kitty! Love it."]},
    {"user": "@Bunny_Gentleman", "img": "宠物3.jpg", "text": "My bunny actually covered its eyes while I was changing clothes! Such a polite boy.", "comments": ["What a gentleman!", "LOL, shy bunny."]},
    {"user": "@LineFriendsFan", "img": "宠物4.jpg", "text": "My puppy looks exactly like the Line Friends dog character!", "comments": ["Identity theft!", "Too perfect, looks like a toy."]},
    {"user": "@Birdy_Sir", "img": "宠物5.jpg", "text": "My little parrot's head is so round, he looks like a true gentleman.", "comments": ["Smart look!", "Very elegant feathers."]},
    {"user": "@Alpaca_Rider", "img": "宠物6.jpg", "text": "Every time I see my alpaca, I feel the urge to jump on and ride it!", "comments": ["Don't do it! Haha", "Iconic fluffy friend."]},
    {"user": "@Piggy_World", "img": "宠物7.jpg", "text": "Pet pigs are actually super cute too. Look at this snout!", "comments": ["Oink oink!", "I want one too!"]},
    {"user": "@Hedgehog_Hero", "img": "宠物8.jpg", "text": "The little hedgehog always messes around while I'm working at my desk.", "comments": ["Spiky coworker!", "My hedgehog does that too!"]}
]

# ==========================================
# 3. PAGE ROUTING LOGIC
# ==========================================

if 'nav' not in st.session_state:
    st.session_state.nav = 'Passport'

# --- SCREEN 1: PET PASSPORT ---
if st.session_state.nav == 'Passport':
    st.image("logo.jpg", width=120)
    st.markdown("# 🐾 Petizen Passport")
    st.write("Welcome! Tell us about your best friend to personalize your experience.")
    
    with st.form("passport_form"):
        st.subheader("Pet Information")
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Pet Name *")
            st.text_input("Fur Color")
        with c2:
            st.text_input("Personality (e.g. Energetic)")
            st.text_input("Dietary Preference")
            
        st.subheader("Owner Information")
        owner_name = st.text_input("Owner Full Name *")
        owner_tel = st.text_input("Contact Phone Number *")
        
        if st.form_submit_button("Create Passport & Enter App"):
            if owner_name and owner_tel:
                st.session_state.user = owner_name
                st.session_state.nav = 'Home'
                st.rerun()
            else:
                st.error("Please fill in the required fields (*).")

# --- SCREEN 2: HOME (12 SHOPS) ---
elif st.session_state.nav == 'Home':
    st.image("logo.jpg", width=80)
    st.markdown(f"## Welcome, {st.session_state.user}! 👋")
    
    # Sorting Filters
    sort_option = st.selectbox("Sort Services By:", 
                               ["Distance (Nearest)", "Rating (Highest)", 
                                "Price (Low to High)", "Price (High to Low)"])
    
    # Sorting Logic
    df_shops = pd.DataFrame(merchants)
    if "Distance" in sort_option: df_shops = df_shops.sort_values("dist")
    elif "Rating" in sort_option: df_shops = df_shops.sort_values("rating", ascending=False)
    elif "Low to High" in sort_option: df_shops = df_shops.sort_values("price")
    elif "High to Low" in sort_option: df_shops = df_shops.sort_values("price", ascending=False)
    
    # Display 12 Shops
    for idx, row in df_shops.iterrows():
        with st.container():
            st.markdown(f"""
            <div class="app-card">
                <img src="{row['img']}" style="width:100%; border-radius:15px; margin-bottom:15px; object-fit: cover; height: 180px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="shop-title">{row['name']}</span>
                    <span style="color:#FF6B6B; font-weight:bold; font-size:18px;">⭐ {row['rating']}</span>
                </div>
                <div style="margin: 10px 0;">
                    <span class="shop-tag">📍 {row['loc']} ({row['dist']}km)</span>
                    <span class="shop-tag">💰 ${row['price']} up</span>
                </div>
                <p style="font-size:15px; color:#2D3436; line-height:1.4;"><b>Services:</b> {row['serv']}</p>
                <p style="font-size:13px; color:#95A5A6;">📞 Tel: {row['tel']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Book Appointment", key=f"shop_{idx}"):
                st.toast(f"Opening booking for {row['name']}...")

# --- SCREEN 3: COUPONS (GROUP BUY) ---
elif st.session_state.nav == 'Coupons':
    st.markdown("## 🎟️ Exclusive Bundle Deals")
    st.write("Group-buy discounts and prepaid packages for extra savings.")
    
    for c in coupons:
        st.markdown(f"""
        <div class="app-card" style="border-left: 10px solid #FF6B6B;">
            <div style="display:flex; justify-content:space-between; align-items: flex-start;">
                <div>
                    <span style="font-weight:bold; font-size:19px;">{c['name']}</span>
                    <p style="color:gray; font-size:13px; margin-top:5px;">{c['desc']}</p>
                </div>
                <span style="background:#FF6B6B; color:white; padding:3px 12px; border-radius:12px; font-size:11px; font-weight:bold;">BUNDLE</span>
            </div>
            <div style="margin-top:15px; display:flex; align-items:baseline;">
                <span style="font-size:28px; font-weight:bold; color:#FF6B6B;">{c['price']}</span>
                <span style="text-decoration:line-through; color:#BDC3C7; font-size:16px; margin-left:10px;">{c['orig']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button(f"Buy Voucher", key=f"cpn_{c['name']}")

# --- SCREEN 4: COMMUNITY (FORUM) ---
elif st.session_state.nav == 'Community':
    st.markdown("## 💬 Petizen Community")
    st.write("Share your pet's daily life and connect with others.")
    
    for p in posts:
        st.markdown(f"""
        <div class="app-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <span class="post-user">{p['user']}</span>
                <div style="display:flex; gap:8px;">
                    <span style="border:1px solid #FF6B6B; padding:2px 10px; border-radius:15px; color:#FF6B6B; font-size:12px; font-weight:bold;">+ Follow</span>
                    <span style="border:1px solid #FF6B6B; padding:2px 10px; border-radius:15px; color:#FF6B6B; font-size:12px; font-weight:bold;">+ Friend</span>
                </div>
            </div>
            <img src="{p['img']}" style="width:100%; border-radius:15px; margin-bottom:12px;">
            <p style="font-size:16px; font-weight:500; color:#2D3436;">{p['text']}</p>
            <hr style="border:0.5px solid #F1F2F6; margin:15px 0;">
            <p style="font-size:12px; font-weight:bold; color:#95A5A6; text-transform:uppercase;">Recent Comments</p>
        """, unsafe_allow_html=True)
        
        for comm in p['comments']:
            st.markdown(f"<div class='comment-box'>{comm}</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 4. BOTTOM NAVIGATION BAR
# ==========================================
st.markdown("<br><br><br>", unsafe_allow_html=True)
col_nav1, col_nav2, col_nav3 = st.columns(3)
with col_nav1:
    if st.button("🏠 Home"): st.session_state.nav = 'Home'; st.rerun()
with col_nav2:
    if st.button("🎟️ Deals"): st.session_state.nav = 'Coupons'; st.rerun()
with col_nav3:
    if st.button("💬 Forum"): st.session_state.nav = 'Community'; st.rerun()

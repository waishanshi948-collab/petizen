import streamlit as st
import pandas as pd

# ==========================================
# 0. PAGE CONFIGURATION & INITIALIZATION
# ==========================================
st.set_page_config(page_title="Petizen App", page_icon="🐾", layout="centered")

# Initialize Session State (To remember user data and navigation)
if 'pet_passport' not in st.session_state:
    st.session_state.pet_passport = None
if 'coupons_wallet' not in st.session_state:
    st.session_state.coupons_wallet = []

# Mock Database for Shops
mock_shops = [
    {"Name": "Pawfect Groomers", "Location": "Causeway Bay", "Distance (km)": 1.2, "Services": "Grooming, Spa", "Rating": 4.9, "Price": "$$"},
    {"Name": "CityVet Clinic", "Location": "Wan Chai", "Distance (km)": 0.8, "Services": "Vet Care, Vaccines", "Rating": 4.8, "Price": "$$$"},
    {"Name": "Happy Paws Daycare", "Location": "Central", "Distance (km)": 2.5, "Services": "Boarding, Play", "Rating": 4.5, "Price": "$$"},
    {"Name": "Pet Uber HK", "Location": "All HK", "Distance (km)": 0.1, "Services": "Pet Transport", "Rating": 4.7, "Price": "$"},
    {"Name": "Dr. Meow Vet Hub", "Location": "Mong Kok", "Distance (km)": 5.0, "Services": "Vet Care, Surgery", "Rating": 4.9, "Price": "$$$"},
    {"Name": "Luxury Fluff Salon", "Location": "Mid-Levels", "Distance (km)": 3.1, "Services": "Premium Grooming", "Rating": 5.0, "Price": "$$$$"}
]
df_shops = pd.DataFrame(mock_shops)

# ==========================================
# 1. SCREEN: PET PASSPORT (ONBOARDING)
# ==========================================
def pet_passport_screen():
    st.title("🐾 Welcome to Petizen")
    st.markdown("### Create Your Pet Passport")
    st.write("Help us personalize your experience. (This data creates user lock-in!)")
    
    with st.form("passport_form"):
        name = st.text_input("Pet Name")
        species = st.selectbox("Species", ["Dog", "Cat", "Rabbit", "Other"])
        age = st.number_input("Age (Years)", min_value=0, max_value=30, step=1)
        gender = st.radio("Gender", ["Male", "Female"])
        vaccinated = st.checkbox("Fully Vaccinated? (Verified for clinics)")
        
        submitted = st.form_submit_button("Save & Enter App")
        if submitted:
            if name == "":
                st.error("Please enter a pet name.")
            else:
                st.session_state.pet_passport = {"Name": name, "Species": species, "Vaccinated": vaccinated}
                st.success("Passport Created!")
                st.rerun() # Refresh page to go to Main App

# ==========================================
# 2. SCREEN: MAIN APP (TABS)
# ==========================================
def main_app():
    st.sidebar.title(f"Hi, {st.session_state.pet_passport['Name']}'s Owner! 🐾")
    if st.session_state.pet_passport['Vaccinated']:
        st.sidebar.success("✅ Vaccine Verified")
    else:
        st.sidebar.warning("⚠️ Vaccine Pending")

    # App Navigation via Tabs
    tab1, tab2, tab3 = st.tabs(["🏪 Services & Booking", "🎟️ Wallet & Coupons", "💬 Community Forum"])

    # ----------------------------------------
    # TAB 1: SERVICES & PRICE COMPARISON
    # ----------------------------------------
    with tab1:
        st.header("Find Services & Products")
        
        # Transparent Price Comparison (Filters)
        col1, col2 = st.columns(2)
        with col1:
            sort_by = st.selectbox("Sort By:", ["Distance (Nearest First)", "Rating (Highest First)"])
        with col2:
            service_filter = st.selectbox("Filter Service:", ["All", "Grooming", "Vet Care", "Boarding", "Transport"])
        
        # Apply Filters
        filtered_df = df_shops.copy()
        if service_filter != "All":
            filtered_df = filtered_df[filtered_df["Services"].str.contains(service_filter)]
        
        if sort_by == "Distance (Nearest First)":
            filtered_df = filtered_df.sort_values(by="Distance (km)")
        else:
            filtered_df = filtered_df.sort_values(by="Rating", ascending=False)

        # Display Shops
        for index, row in filtered_df.iterrows():
            with st.container():
                st.markdown(f"### {row['Name']}")
                st.markdown(f"📍 **{row['Location']}** ({row['Distance (km)']} km) | ⭐ **{row['Rating']}** | 💰 **{row['Price']}**")
                st.write(f"🛠️ Services: {row['Services']}")
                
                # Booking & Cross-Selling Logic
                if st.button(f"Book {row['Name']}", key=f"book_{index}"):
                    st.balloons()
                    st.success(f"🎉 Booking Confirmed at {row['Name']}!")
                    
                    # Map/Cross-Sell Logic: Recommend Pet Ride after booking
                    if "Grooming" in row['Services'] or "Vet" in row['Services']:
                        st.info("🚗 **Smart Recommendation:** Need a ride there? We just added a **20% OFF Pet Uber Coupon** to your wallet!")
                        if "20% OFF Pet Ride" not in st.session_state.coupons_wallet:
                            st.session_state.coupons_wallet.append("20% OFF Pet Ride")

                st.divider()

    # ----------------------------------------
    # TAB 2: COUPONS & CASH FLOW
    # ----------------------------------------
    with tab2:
        st.header("My Wallet & Coupons")
        
        st.subheader("Your Active Coupons")
        if len(st.session_state.coupons_wallet) == 0:
            st.write("No active coupons. Book a service to get rewards!")
        else:
            for coupon in st.session_state.coupons_wallet:
                st.success(f"🎟️ **{coupon}** - Ready to use!")
                
        st.divider()
        
        # Cash Flow Guarantee: Prepaid Coupons
        st.subheader("Buy Prepaid Packages (Save More!)")
        st.write("Secure funds upfront to guarantee high-quality services.")
        
        col_pkg1, col_pkg2 = st.columns(2)
        with col_pkg1:
            st.info("✂️ **10 Grooming Sessions**\n\n$3000 (Save $500)")
            if st.button("Buy Grooming Package"):
                st.success("Purchased successfully!")
        with col_pkg2:
            st.info("🩺 **Annual Vet Care**\n\nIncludes vaccines & 2 checkups.")
            if st.button("Buy Vet Package"):
                st.success("Purchased successfully!")

    # ----------------------------------------
    # TAB 3: COMMUNITY & FORUM
    # ----------------------------------------
    with tab3:
        st.header("Petizen Community")
        forum_type = st.radio("Select Category:", ["❓ Q&A (Help & Advice)", "📸 Daily Life"])
        
        if forum_type == "❓ Q&A (Help & Advice)":
            st.markdown("#### Top Questions Today")
            with st.expander("🐶 @Milo_Mom: Help! My Golden Retriever seems sad today."):
                st.write("**Problem:** He hasn't eaten his food and is just lying by the door. What should I do?")
                st.markdown("---")
                st.write("**Dr. Vet (Verified):** Hi! It could be the hot weather, but if he hasn't eaten for 24 hours, please book a quick consultation.")
                st.write("**@CorgiLover:** Try giving him some boiled chicken! Worked for mine.")
                
            with st.expander("🐱 @CatDad: Best cat litter for small Hong Kong apartments?"):
                st.write("**Problem:** Looking for something that controls odor perfectly.")
                st.markdown("---")
                st.write("**@LunaTheCat:** Highly recommend Tofu litter! You can buy it in the Petizen store.")

        else:
            st.markdown("#### Pet Daily Life")
            st.image("https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&w=600&q=80", caption="Sunbathing by the window ☀️ - @LunaTheCat")
            st.write("❤️ 96 Likes  💬 12 Comments")
            st.markdown("---")
            st.image("https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?auto=format&fit=crop&w=600&q=80", caption="Fresh after the spa! 🎀 - @CocoLife")
            st.write("❤️ 152 Likes  💬 21 Comments")

# ==========================================
# APP ROUTING LOGIC
# ==========================================
if st.session_state.pet_passport is None:
    pet_passport_screen()
else:
    main_app()

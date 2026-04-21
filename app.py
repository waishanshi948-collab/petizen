import streamlit as st
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="Petizen - 宠物一站式服务平台",
    page_icon="🐾",
    layout="wide"
)

# 侧边栏导航
with st.sidebar:
    st.markdown("# 🐾 Petizen")
    page = st.radio("导航", ["🏠 主页", "📅 我的预订", "👥 社区", "🛍️ 商店", "👤 个人资料"])

# 主页
if page == "🏠 主页":
    st.title("🐾 Petizen")
    st.markdown("## 一切为了您的宠物")
    
    # 快捷服务
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("🏥 兽医护理", use_container_width=True)
    with col2:
        st.button("✂️ 美容护理", use_container_width=True)
    with col3:
        st.button("🚗 宠物接送", use_container_width=True)
    
    # 即将到来的预订
    st.markdown("## 📅 即将到来的预订")
    booking_data = {
        "服务": ["美容护理", "兽医咨询", "宠物接送"],
        "地点": ["铜锣湾", "湾仔", "大坑"],
        "日期": ["5月18日", "5月20日", "5月21日"],
        "状态": ["✅ 已确认", "✅ 已确认", "⏰ 待确认"]
    }
    st.table(booking_data)
    
    # 社区帖子
    st.markdown("## 👥 宠物社区")
    posts = [
        "🐕 Milo: 周末在维多利亚公园玩得超开心！❤️ 128",
        "🐱 Luna: 窗边晒太阳好舒服 🌞 96",
        "🐕 Bruno: 探索大坑新地方 🐾 152"
    ]
    for post in posts:
        st.text(post)

elif page == "📅 我的预订":
    st.title("📅 预订服务")
    service = st.selectbox("选择服务", ["兽医护理", "美容护理", "宠物日托", "宠物接送"])
    date = st.date_input("选择日期")
    if st.button("确认预订"):
        st.success(f"成功预订 {service}！")

elif page == "👥 社区":
    st.title("👥 宠物社区")
    post = st.text_area("分享你的故事")
    if st.button("发布"):
        st.success("发布成功！")

elif page == "🛍️ 商店":
    st.title("🛍️ 宠物商店")
    products = [" premium狗粮 $299", "猫咪玩具 $79", "宠物床 $399"]
    for product in products:
        if st.button(product):
            st.success(f"已添加 {product} 到购物车")

elif page == "👤 个人资料":
    st.title("👤 我的资料")
    st.markdown("""
    - 姓名: 宠物家长
    - 邮箱: petlover@example.com
    - 电话: +852 1234 5678
    - 宠物: Max (狗狗, 3岁)
    """)

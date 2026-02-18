import streamlit as st
import pandas as pd
from datetime import datetime

# --- การตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="Lost & Found Center", page_icon="🔍", layout="wide")

# --- ส่วนของสไตล์ (Custom CSS สำหรับโทนฟ้า-ขาว) ---
st.markdown("""
    <style>
    .main {
        background-color: #f0f8ff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        border: 1px solid #007bff;
        background-color: #007bff;
        color: white;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        color: white;
    }
    .lost-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 10px solid #ff4b4b;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .found-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 10px solid #28a745;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ระบบจัดการข้อมูล (จำลอง) ---
# ในอนาคตสามารถเชื่อมต่อ Google Sheets ได้ที่นี่
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['ประเภท', 'ชื่อสิ่งของ', 'สถานที่', 'รายละเอียด', 'ติดต่อ', 'วันที่'])

# --- ส่วนหัวของเว็บ ---
st.title("🔍 ศูนย์รวมแจ้งของหาย - เก็บได้")
st.subheader("Community Lost & Found Service")

# --- เมนูแถบข้าง (Sidebar) สำหรับแจ้งข้อมูล ---
with st.sidebar:
    st.header("📢 แจ้งข้อมูลใหม่")
    report_type = st.radio("ประเภทการแจ้ง", ["ของหาย", "เก็บได้"])
    item_name = st.text_input("ชื่อสิ่งของ")
    location = st.text_input("สถานที่")
    description = st.text_area("รายละเอียดเพิ่มเติม")
    contact = st.text_input("เบอร์ติดต่อ / Line ID")
    
    if st.button("บันทึกข้อมูล"):
        if item_name and contact:
            new_data = {
                'ประเภท': report_type,
                'ชื่อสิ่งของ': item_name,
                'สถานที่': location,
                'รายละเอียด': description,
                'ติดต่อ': contact,
                'วันที่': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.data = pd.concat([pd.DataFrame([new_data]), st.session_state.data], ignore_index=True)
            st.success("บันทึกข้อมูลสำเร็จ!")
        else:
            st.error("กรุณากรอกชื่อสิ่งของและข้อมูลติดต่อ")

# --- ส่วนแสดงผลหลัก ---
tab1, tab2, tab3 = st.tabs(["ทั้งหมด", "📌 ของหาย (Lost)", "✅ เก็บได้ (Found)"])

def display_items(df):
    if df.empty:
        st.write("ยังไม่มีข้อมูลในขณะนี้")
    else:
        for index, row in df.iterrows():
            card_class = "lost-card" if row['ประเภท'] == "ของหาย" else "found-card"
            st.markdown(f"""
                <div class="{card_class}">
                    <h4>{row['ประเภท']}: {row['ชื่อสิ่งของ']}</h4>
                    <p><b>📍 สถานที่:</b> {row['สถานที่']}</p>
                    <p><b>📝 รายละเอียด:</b> {row['รายละเอียด']}</p>
                    <p><b>📞 ติดต่อ:</b> {row['ติดต่อ']}</p>
                    <small>📅 วันที่แจ้ง: {row['วันที่']}</small>
                </div>
            """, unsafe_allow_html=True)

with tab1:
    display_items(st.session_state.data)

with tab2:
    display_items(st.session_state.data[st.session_state.data['ประเภท'] == "ของหาย"])

with tab3:
    display_items(st.session_state.data[st.session_state.data['ประเภท'] == "เก็บได้"])

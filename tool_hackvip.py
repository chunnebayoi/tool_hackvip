import streamlit as st
import hashlib
from collections import deque, Counter

# ---------------- ĐĂNG NHẬP ------------------
valid_accounts = {
    "admin": {"password": "123456", "key": "VIP123"},
    "kanhao": {"password": "888888", "key": "SUNWIN"},
    "test": {"password": "abc123", "key": "FREE68"},
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login_ui():
    st.title("🔐 Đăng nhập hệ thống")
    username = st.text_input("👤 Tài khoản")
    password = st.text_input("🔑 Mật khẩu", type="password")
    key = st.text_input("🧾 Mã kích hoạt")

    if st.button("🚪 Đăng nhập"):
        if username in valid_accounts:
            if (valid_accounts[username]["password"] == password and
                valid_accounts[username]["key"] == key):
                st.success("✅ Đăng nhập thành công!")
                st.session_state.authenticated = True
            else:
                st.error("❌ Sai mật khẩu hoặc mã kích hoạt.")
        else:
            st.error("❌ Tài khoản không tồn tại.")

if not st.session_state.authenticated:
    login_ui()
    st.stop()

# --------------- TOOL CHÍNH -------------------

st.title("🎲 Dự Đoán Tài Xỉu & Phân Tích Cầu SUNWIN")
st.caption("Zalo 0332066509 - Phiên bản nâng cấp")

def complex_calculation(input_str: str) -> float:
    sha256_hash = int(hashlib.sha256(input_str.encode()).hexdigest(), 16)
    blake2b_hash = int(hashlib.blake2b(input_str.encode()).hexdigest(), 16)
    combined_hash = (
        sha256_hash * 0.4 +
        blake2b_hash % 100 * 0.6
    )
    return combined_hash % 100

def bayesian_adjustment(recent_results: deque) -> float:
    count = Counter(recent_results)
    total = len(recent_results)
    if total == 0:
        return 50.0
    prob_xiu = (count["Xiu"] + 1) / (total + 2)
    return prob_xiu * 100

def detect_trend(recent_results: deque) -> str:
    if len(recent_results) < 4:
        return "Không đủ dữ liệu phân tích cầu."
    trend_str = "".join(["T" if res == "Tài" else "X" for res in recent_results])
    if trend_str.endswith("TTTT"):
        return "Cầu bệt Tài"
    elif trend_str.endswith("XXXX"):
        return "Cầu bệt Xỉu"
    return "Không phát hiện cầu đặc biệt."

# --- Giao diện nhập liệu ---
player_name = st.text_input("🔑 Tên người chơi:", value="Ẩn danh")
code_input = st.text_input("🧠 Nhập mã phiên hoặc chuỗi bất kỳ:")
mode = st.radio("🎯 Chế độ phân tích:", ["Cơ bản", "Nâng cao (AI + Phân tích cầu)"])

if code_input:
    result = "Tài" if complex_calculation(code_input) > 50 else "Xỉu"
    st.subheader(f"✅ Kết quả dự đoán: {result}")

    if mode == "Nâng cao (AI + Phân tích cầu)":
        if "history" not in st.session_state:
            st.session_state.history = deque(maxlen=10)

        st.session_state.history.append(result)
        trend = detect_trend(st.session_state.history)
        prob = bayesian_adjustment(st.session_state.history)

        st.info(f"📈 Phân tích cầu: {trend}")
        st.info(f"📊 Xác suất Xỉu (theo lịch sử): {prob:.2f}%")


# QUAN LY DIEM SINH VIEN - STREAMLIT

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cau hinh trang
st.set_page_config(
    page_title="Quan ly diem sinh vien",
    page_icon="📚",
    layout="wide"
)

# Tieu de
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.write("Bảng điểm, kết quả học tập và thống kê lớp học.")

# Tao du lieu
data = {
    "Ho_ten": [
        "Nguyen An", "Tran Binh", "Le Chi", "Pham Dung",
        "Hoang Giang", "Vo Hanh", "Do Khoa", "Bui Lan",
        "Dang Minh", "Ngo Phuong"
    ],
    "Chuyen_can": [9, 8, 7, 10, 6, 8, 5, 9, 7, 10],
    "Giua_ky":    [8, 7, 6, 9, 5, 8, 4, 9, 7, 8],
    "Cuoi_ky":    [9, 8, 7, 10, 6, 9, 5, 8, 6, 9]
}

df = pd.DataFrame(data)

# Tinh diem tong ket
df["Tong_ket"] = (
    0.2 * df["Chuyen_can"]
    + 0.3 * df["Giua_ky"]
    + 0.5 * df["Cuoi_ky"]
).round(2)

# Xep loai
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# Bang diem
st.subheader("1. Bảng điểm sinh viên")

bang_hien_thi = df.rename(columns={
    "Ho_ten": "Họ tên",
    "Chuyen_can": "Chuyên cần",
    "Giua_ky": "Giữa kỳ",
    "Cuoi_ky": "Cuối kỳ",
    "Tong_ket": "Tổng kết",
    "Xep_loai": "Xếp loại"
})

st.dataframe(
    bang_hien_thi,
    use_container_width=True,
    hide_index=True
)

# Thong ke
diem_tb = df["Tong_ket"].mean()
sv_max = df.loc[df["Tong_ket"].idxmax()]
sv_min = df.loc[df["Tong_ket"].idxmin()]
so_dat = int((df["Tong_ket"] >= 5).sum())

st.subheader("2. Thống kê kết quả học tập")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Điểm trung bình", f"{diem_tb:.2f}")
c2.metric("Số sinh viên đạt", f"{so_dat}/10")
c3.metric("Điểm cao nhất", f"{sv_max['Tong_ket']:.2f}")
c4.metric("Điểm thấp nhất", f"{sv_min['Tong_ket']:.2f}")

st.write(
    f"**Sinh viên điểm cao nhất:** "
    f"{sv_max['Ho_ten']} ({sv_max['Tong_ket']:.2f})"
)

st.write(
    f"**Sinh viên điểm thấp nhất:** "
    f"{sv_min['Ho_ten']} ({sv_min['Tong_ket']:.2f})"
)

# Chon sinh vien
st.subheader("3. Tra cứu điểm sinh viên")

ten_sv = st.selectbox(
    "Chọn sinh viên:",
    df["Ho_ten"].tolist()
)

sv = df[df["Ho_ten"] == ten_sv].iloc[0]

st.write(f"**Họ tên:** {sv['Ho_ten']}")

d1, d2, d3, d4 = st.columns(4)

d1.metric("Chuyên cần", f"{sv['Chuyen_can']:.2f}")
d2.metric("Giữa kỳ", f"{sv['Giua_ky']:.2f}")
d3.metric("Cuối kỳ", f"{sv['Cuoi_ky']:.2f}")
d4.metric("Tổng kết", f"{sv['Tong_ket']:.2f}")

st.write(f"**Xếp loại:** {sv['Xep_loai']}")

# Bieu do
st.subheader("4. Biểu đồ điểm tổng kết")

fig, ax = plt.subplots(figsize=(12, 6))

ax.bar(
    df["Ho_ten"],
    df["Tong_ket"],
    edgecolor="black"
)

ax.set_title("ĐIỂM TỔNG KẾT CỦA 10 SINH VIÊN")
ax.set_xlabel("Họ tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
ax.tick_params(axis="x", labelrotation=45)

for i, diem in enumerate(df["Tong_ket"]):
    ax.text(i, diem + 0.1, f"{diem:.2f}", ha="center")

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Thong tin nguoi tao
st.divider()
st.caption("Người tạo ứng dụng: [LÊ THỊ THÙY DƯƠNG] | MSSV: [024308002055]")

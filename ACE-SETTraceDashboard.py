import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import urllib.parse

# Konfigurasi Halaman Dashboard (Eksklusif Pentadbir & Pemantau)
st.set_page_config(
    page_title="ACE-SET Trace 2.0 - Dashboard Pentadbir", 
    page_icon="🏥", 
    layout="wide"
)

# --- 1. PANGKALAN DATA SIMULASI (SESSION STATE) ---
if 'assets_data' not in st.session_state:
    st.session_state['assets_data'] = pd.DataFrame({
        'Kod_QR': ['QR-OT1-001', 'QR-OT2-002', 'QR-CSSD-003', 'QR-EMER-004', 'QR-OT1-005'],
        'ID_Aset': ['AST-001', 'AST-002', 'AST-003', 'AST-004', 'AST-005'],
        'Nama_Aset': ['Portable Ultrasound', 'Infusion Pump', 'Laryngoscope', 'Defibrillator', 'Patient Monitor'],
        'Unit': ['Dewan Bedah 1', 'Dewan Bedah 2', 'CSSD', 'Kecemasan', 'Dewan Bedah 1'],
        'Peminjam': ['Dr. Ahmad', 'JU Siti', 'Dr. Lee', 'JU Ali', 'Dr. Rahman'],
        'No_Telefon': ['60123456789', '60139876543', '60112233445', '60198877665', '60176655443'],
        'Status': ['Keluar', 'Keluar', 'Masuk', 'Keluar', 'Masuk'],
        'Tarikh_Jangka_Pulang': [
            datetime.now() - timedelta(hours=6), # Dalam tempoh 12 jam (Peringatan Awal)
            datetime.now() - timedelta(hours=30), # Lewat > 24 jam (Amaran WhatsApp!)
            datetime.now() + timedelta(days=2), 
            datetime.now() - timedelta(hours=48), # Lewat > 24 jam (Amaran WhatsApp!)
            datetime.now() + timedelta(days=3)
        ]
    })

df = st.session_state['assets_data']

# --- 2. HEADER UTAMA DASHBOARD ---
st.title("📊 Dashboard Pemantauan: ACE-SET Trace 2.0")
st.markdown("Sistem Pengesanan & Kawalan Pergerakan Aset Alih Dewan Bedah Hospital Bintulu (Eksklusif Pentadbir & Pemantau).")
st.markdown("---")

# --- 3. METRIK UTAMA RINGKASAN ---
col1, col2, col3, col4, col5 = st.columns(5)
total_aset = len(df)
aset_keluar = len(df[df['Status'] == 'Keluar'])
aset_masuk = len(df[df['Status'] == 'Masuk'])

# Pengiraan masa untuk Peringatan (12 Jam) & Amaran (> 24 Jam)
waktu_semasa = datetime.now()
df['Tarikh_Jangka_Pulang'] = pd.to_datetime(df['Tarikh_Jangka_Pulang'])

# Logik 1: Peringatan 12 Jam sebelum tarikh jangka pulang
selisih_masa = (df['Tarikh_Jangka_Pulang'] - waktu_semasa)
kategori_peringatan_12j = df[(df['Status'] == 'Keluar') & (selisih_masa <= timedelta(hours=12)) & (selisih_masa > timedelta(hours=0))]
jumlah_peringatan = len(kategori_peringatan_12j)

# Logik 2: Amaran WhatsApp jika lewat > 24 jam daripada tarikh jangka pulang
kategori_amaran_24j = df[(df['Status'] == 'Keluar') & (waktu_semasa - df['Tarikh_Jangka_Pulang'] >= timedelta(hours=24))]
jumlah_amaran = len(kategori_amaran_24j)

col1.metric("Jumlah Rekod Aset", total_aset)
col2.metric("Aset Sedang Keluar", aset_keluar)
col3.metric("Aset Dalam Stor (Masuk)", aset_masuk)
col4.metric("🔔 Peringatan (12 Jam)", jumlah_peringatan)
col5.metric("🚨 Amaran (>24 Jam)", jumlah_amaran, delta_color="inverse")

st.markdown("---")

# --- 4. GRAF ANALISIS AUTOMATIK ---
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("📈 Taburan Status Aset")
    status_counts = df['Status'].value_counts()
    st.bar_chart(status_counts)

with col_g2:
    st.subheader("📊 Taburan Aset Mengikut Unit")
    unit_counts = df['Unit'].value_counts()
    st.bar_chart(unit_counts)

st.markdown("---")

# --- 5. MODUL NOTIFIKASI & AMARAN PEMINJAM ---
st.subheader("🚨 Modul Tindakan & Notifikasi Peminjam")

tab_warn, tab_rem = st.tabs(["⚠️ Amaran WhatsApp (>24 Jam Lewat)", "🔔 Peringatan Awal (12 Jam Sebelum Pulang)"])

with tab_warn:
    st.markdown("Aset berikut telah lewat dipulangkan **melebihi 24 jam**. Klik butang untuk menghantar mesej amaran terus ke WhatsApp peminjam.")
    
    if jumlah_amaran > 0:
        for index, row in kategori_amaran_24j.iterrows():
            pesan_whatsapp = (
                f"Assalamualaikum / Selamat sejahtera {row['Peminjam']}, "
                f"untuk makluman, aset *{row['Nama_Aset']}* (ID: {row['ID_Aset']}) dari unit *{row['Unit']}* "
                f"telah lewat dipulangkan melebihi 24 jam daripada tarikh jangkaan ({row['Tarikh_Jangka_Pulang'].strftime('%d-%m-%Y %H:%M')}). "
                f"Sila pulangkan segera ke unit."
            )
            encoded_msg = urllib.parse.quote(pesan_whatsapp)
            link_wa = f"https://wa.me/{row['No_Telefon']}?text={encoded_msg}"
            
            col_info, col_btn = st.columns([3, 1])
            with col_info:
                st.error(f"**Aset:** {row['Nama_Aset']} ({row['ID_Aset']}) | **Unit:** {row['Unit']} | **Peminjam:** {row['Peminjam']} | **Jangka Pulang:** {row['Tarikh_Jangka_Pulang'].strftime('%d-%m-%Y %H:%M')}")
            with col_btn:
                st.markdown(f"[ Hantar WhatsApp 📲 ]({link_wa})", unsafe_allow_html=True)
    else:
        st.success("Syabas! Tiada aset yang lewat melebihi 24 jam setakat ini.")

with tab_rem:
    st.markdown("Senarai aset yang perlu dipulangkan dalam tempoh **12 jam lagi** (Peringatan awal kepada peminjam).")
    
    if jumlah_peringatan > 0:
        tabel_peringatan = kategori_peringatan_12j[['ID_Aset', 'Nama_Aset', 'Unit', 'Peminjam', 'No_Telefon', 'Tarikh_Jangka_Pulang']]
        st.dataframe(tabel_peringatan, use_container_width=True)
    else:
        st.info("Tiada peringatan 12 jam diperlukan buat masa ini.")

st.markdown("---")

# --- 6. SENARAI REKOD PENUH KESELURUHAN ---
st.subheader("📋 Pangkalan Data Keseluruhan Pergerakan Aset")
st.dataframe(df, use_container_width=True)

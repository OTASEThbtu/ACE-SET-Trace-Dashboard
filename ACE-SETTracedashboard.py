import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import urllib.parse
# Konfigurasi Halaman Dashboard (Eksklusif Pentadbir &amp; Pemantau)
st.set_page_config(
page_title=&quot;ACE-SET Trace 2.0 - Dashboard Pentadbir&quot;,
page_icon=&quot;��&quot;
layout=&quot;wide&quot;
)
# --- 1. PANGKALAN DATA SIMULASI (SESSION STATE) ---
if &#39;assets_data&#39; not in st.session_state:
st.session_state[&#39;assets_data&#39;] = pd.DataFrame({
&#39;Kod_QR&#39;: [&#39;QR-OT1-001&#39;, &#39;QR-OT2-002&#39;, &#39;QR-CSSD-003&#39;, &#39;QR-
EMER-004&#39;, &#39;QR-OT1-005&#39;],
&#39;ID_Aset&#39;: [&#39;AST-001&#39;, &#39;AST-002&#39;, &#39;AST-003&#39;, &#39;AST-004&#39;, &#39;AST-
005&#39;],
&#39;Nama_Aset&#39;: [&#39;Portable Ultrasound&#39;, &#39;Infusion Pump&#39;,
&#39;Laryngoscope&#39;, &#39;Defibrillator&#39;, &#39;Patient Monitor&#39;],
&#39;Unit&#39;: [&#39;Dewan Bedah 1&#39;, &#39;Dewan Bedah 2&#39;, &#39;CSSD&#39;,
&#39;Kecemasan&#39;, &#39;Dewan Bedah 1&#39;],
&#39;Peminjam&#39;: [&#39;Dr. Ahmad&#39;, &#39;JU Siti&#39;, &#39;Dr. Lee&#39;, &#39;JU Ali&#39;, &#39;Dr.
Rahman&#39;],
&#39;No_Telefon&#39;: [&#39;60123456789&#39;, &#39;60139876543&#39;, &#39;60112233445&#39;,
&#39;60198877665&#39;, &#39;60176655443&#39;],
&#39;Status&#39;: [&#39;Keluar&#39;, &#39;Keluar&#39;, &#39;Masuk&#39;, &#39;Keluar&#39;, &#39;Masuk&#39;],
&#39;Tarikh_Jangka_Pulang&#39;: [
datetime.now() - timedelta(hours=6), # Dalam tempoh 12
jam (Peringatan Awal)
datetime.now() - timedelta(hours=30), # Lewat &gt; 24 jam
(Amaran WhatsApp!)
datetime.now() + timedelta(days=2),
datetime.now() - timedelta(hours=48), # Lewat &gt; 24 jam
(Amaran WhatsApp!)
datetime.now() + timedelta(days=3)
]
})
df = st.session_state[&#39;assets_data&#39;]
# --- 2. HEADER UTAMA DASHBOARD ---
st.title(&quot;�� Dashboard Pemantauan: ACE-SET Trace 2.0&quot;)
st.markdown(&quot;Sistem Pengesanan &amp; Kawalan Pergerakan Aset Alih Dewan

Bedah Hospital Bintulu (Eksklusif Pentadbir &amp; Pemantau).&quot;)
st.markdown(&quot;---&quot;)
# --- 3. METRIK UTAMA RINGKASAN ---
col1, col2, col3, col4, col5 = st.columns(5)
total_aset = len(df)
aset_keluar = len(df[df[&#39;Status&#39;] == &#39;Keluar&#39;])
aset_masuk = len(df[df[&#39;Status&#39;] == &#39;Masuk&#39;])
# Pengiraan masa untuk Peringatan (12 Jam) &amp; Amaran (&gt; 24 Jam)
waktu_semasa = datetime.now()
df[&#39;Tarikh_Jangka_Pulang&#39;] =
pd.to_datetime(df[&#39;Tarikh_Jangka_Pulang&#39;])
# Logik 1: Peringatan 12 Jam sebelum tarikh jangka pulang
selisih_masa = (df[&#39;Tarikh_Jangka_Pulang&#39;] - waktu_semasa)
kategori_peringatan_12j = df[(df[&#39;Status&#39;] == &#39;Keluar&#39;) &amp;
(selisih_masa &lt;= timedelta(hours=12)) &amp; (selisih_masa &gt;
timedelta(hours=0))]
jumlah_peringatan = len(kategori_peringatan_12j)
# Logik 2: Amaran WhatsApp jika lewat &gt; 24 jam daripada tarikh jangka
pulang
kategori_amaran_24j = df[(df[&#39;Status&#39;] == &#39;Keluar&#39;) &amp; (waktu_semasa -
df[&#39;Tarikh_Jangka_Pulang&#39;] &gt;= timedelta(hours=24))]
jumlah_amaran = len(kategori_amaran_24j)
col1.metric(&quot;Jumlah Rekod Aset&quot;, total_aset)
col2.metric(&quot;Aset Sedang Keluar&quot;, aset_keluar)
col3.metric(&quot;Aset Dalam Stor (Masuk)&quot;, aset_masuk)
col4.metric(&quot;�� Peringatan (12 Jam)&quot;, jumlah_peringatan)
col5.metric(&quot;�� Amaran (&gt;24 Jam)&quot;, jumlah_amaran
delta_color=&quot;inverse&quot;)
st.markdown(&quot;---&quot;)
# --- 4. GRAF ANALISIS AUTOMATIK ---
col_g1, col_g2 = st.columns(2)
with col_g1:
st.subheader(&quot;�� Taburan Status Aset&quot;)
status_counts = df[&#39;Status&#39;].value_counts()
st.bar_chart(status_counts)
with col_g2:
st.subheader(&quot;�� Taburan Aset Mengikut Unit&quot;)
unit_counts = df[&#39;Unit&#39;].value_counts()
st.bar_chart(unit_counts)
st.markdown(&quot;---&quot;)
# --- 5. MODUL NOTIFIKASI &amp; AMARAN PEMINJAM ---

st.subheader(&quot;�� Modul Tindakan &amp; Notifikasi Peminjam&quot;)
tab_warn, tab_rem = st.tabs([&quot;⚠️ Amaran WhatsApp (&gt;24 Jam Lewat)&quot;, &quot;�
Peringatan Awal (12 Jam Sebelum Pulang)&quot;])
with tab_warn:
st.markdown(&quot;Aset berikut telah lewat dipulangkan **melebihi 24
jam**. Klik butang untuk menghantar mesej amaran terus ke WhatsApp
peminjam.&quot;)
if jumlah_amaran &gt; 0:
for index, row in kategori_amaran_24j.iterrows():
pesan_whatsapp = (
f&quot;Assalamualaikum / Selamat sejahtera
{row[&#39;Peminjam&#39;]}, &quot;
f&quot;untuk makluman, aset *{row[&#39;Nama_Aset&#39;]}* (ID:
{row[&#39;ID_Aset&#39;]}) dari unit *{row[&#39;Unit&#39;]}* &quot;
f&quot;telah lewat dipulangkan melebihi 24 jam daripada
tarikh jangkaan ({row[&#39;Tarikh_Jangka_Pulang&#39;].strftime(&#39;%d-%m-%Y
%H:%M&#39;)}). &quot;
f&quot;Sila pulangkan segera ke unit.&quot;
)
encoded_msg = urllib.parse.quote(pesan_whatsapp)
link_wa =
f&quot;https://wa.me/{row[&#39;No_Telefon&#39;]}?text={encoded_msg}&quot;
col_info, col_btn = st.columns([3, 1])
with col_info:
st.error(f&quot;**Aset:** {row[&#39;Nama_Aset&#39;]}
({row[&#39;ID_Aset&#39;]}) | **Unit:** {row[&#39;Unit&#39;]} | **Peminjam:**
{row[&#39;Peminjam&#39;]} | **Jangka Pulang:**
{row[&#39;Tarikh_Jangka_Pulang&#39;].strftime(&#39;%d-%m-%Y %H:%M&#39;)}&quot;)
with col_btn:
st.markdown(f&quot;[ Hantar WhatsApp �� ]({link_wa})&quot;
unsafe_allow_html=True)
else:
st.success(&quot;Syabas! Tiada aset yang lewat melebihi 24 jam
setakat ini.&quot;)
with tab_rem:
st.markdown(&quot;Senarai aset yang perlu dipulangkan dalam tempoh **12
jam lagi** (Peringatan awal kepada peminjam).&quot;)
if jumlah_peringatan &gt; 0:
tabel_peringatan = kategori_peringatan_12j[[&#39;ID_Aset&#39;,
&#39;Nama_Aset&#39;, &#39;Unit&#39;, &#39;Peminjam&#39;, &#39;No_Telefon&#39;,
&#39;Tarikh_Jangka_Pulang&#39;]]
st.dataframe(tabel_peringatan, use_container_width=True)
else:
st.info(&quot;Tiada peringatan 12 jam diperlukan buat masa ini.&quot;)
st.markdown(&quot;---&quot;)

# --- 6. SENARAI REKOD PENUH KESELURUHAN ---
st.subheader(&quot;�� Pangkalan Data Keseluruhan Pergerakan Aset&quot;)
st.dataframe(df, use_container_width=True)

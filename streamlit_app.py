import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="Fashion Lens", layout="wide")

st.title("📸 Fashion Lens: Upload & Get Recommendations")
st.write("Upload gambar pakaian Anda (max 200MB) dan dapatkan rekomendasi pakaian serupa!")

# Sidebar config
api_url = st.sidebar.text_input("Flask API URL", "http://127.0.0.1:5001/upload_image")

# Menggunakan file_uploader untuk upload gambar
uploaded_file = st.file_uploader("Pilih gambar pakaian", type=['jpg', 'png', 'jpeg'], accept_multiple_files=False)

if uploaded_file is not None:
    # Menampilkan gambar yang diupload
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar yang diupload", use_column_width=True)
    
    # Menampilkan progress saat memproses gambar
    with st.spinner('Menganalisis gaya pakaian...'):
        # Konversi gambar ke bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_bytes = img_byte_arr.getvalue()

        files = {'image': (uploaded_file.name, img_bytes, 'image/jpeg')}

        try:
            response = requests.post(api_url, files=files)

            if response.status_code == 200:
                data = response.json()
                recs = data.get('recommendations', [])
                dominant_color = data.get('dominant_color', '')

                st.success(f"Berhasil menganalisis! Warna dominan: {dominant_color}. Ditemukan {len(recs)} produk serupa:")

                # Layout hasil rekomendasi
                cols = st.columns(3)
                for idx, item in enumerate(recs):
                    with cols[idx % 3]:
                        # Menampilkan info produk
                        st.markdown(f"### {item.get('productDisplayName', 'Produk')}")
                        st.write(f"**Warna:** {item.get('baseColour')}")
                        st.write(f"**Kategori:** {item.get('articleType')}")
                        st.write(f"**Musim:** {item.get('season')}")
                        st.write(f"**Penggunaan:** {item.get('usage')}")
                        st.divider()
            else:
                st.error(f"Gagal menghubungi server: {response.status_code}")
        except Exception as e:
            st.error(f"Koneksi ke Backend terputus: {e}")

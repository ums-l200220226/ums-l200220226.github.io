from metaflow import FlowSpec, step, Parameter
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

# Fungsi untuk membersihkan teks
def clean_text(text):
    # Hilangkan emoji dan karakter non-teks
    text = re.sub(r'[\U00010000-\U0010FFFF]', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    # Ubah teks menjadi huruf kecil
    return text.lower()

class WhatsAppClusteringFlow(FlowSpec):

    n_clusters = Parameter('n_clusters', help='Jumlah klaster', default=3)
    output_csv = Parameter('output_csv', help='File output untuk hasil klastering', default='hasil_klaster.csv')

    @step
    def start(self):
        """Baca data dari file log WhatsApp."""
        self.data_file = 'data_group.txt'
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.data_file} tidak ditemukan.")
        except Exception as e:
            raise Exception(f"Terjadi kesalahan saat membaca file: {e}")

        # Parsing pesan dari log WhatsApp
        data = []
        for line in lines:
            match = re.match(r'\d{2}/\d{2}/\d{2} \d{2}\.\d{2} - (.*?): (.*)', line)
            if match:
                sender, message = match.groups()
                data.append({'sender': sender, 'message': message})

        self.data = pd.DataFrame(data)

        if self.data.empty:
            raise ValueError("Log WhatsApp tidak mengandung pesan yang valid.")

        print(f"Data dimuat dengan {len(self.data)} pesan.")
        self.next(self.clean_data)

    @step
    def clean_data(self):
        """Bersihkan pesan dari teks."""
        self.data['cleaned_message'] = self.data['message'].apply(clean_text)

        # Hapus pesan kosong setelah pembersihan
        self.data = self.data[self.data['cleaned_message'].str.strip() != '']

        if self.data.empty:
            raise ValueError("Semua pesan kosong setelah pembersihan.")

        print(f"Data setelah pembersihan: {len(self.data)} pesan.")
        self.next(self.vectorize_data)

    @step
    def vectorize_data(self):
        """Konversi pesan menjadi vektor menggunakan TF-IDF."""
        self.vectorizer = TfidfVectorizer()
        self.vectors = self.vectorizer.fit_transform(self.data['cleaned_message'])
        print(f"TF-IDF menghasilkan matriks dengan bentuk {self.vectors.shape}.")
        self.next(self.cluster_data)

    @step
    def cluster_data(self):
        """Lakukan klasterisasi menggunakan KMeans."""
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        self.data['cluster'] = kmeans.fit_predict(self.vectors)

        # Debugging: Tampilkan jumlah pesan per klaster
        print(self.data['cluster'].value_counts())
        self.kmeans = kmeans
        self.next(self.top_words)

    @step
    def top_words(self):
        """Tampilkan 3 kata teratas untuk setiap klaster."""
        terms = self.vectorizer.get_feature_names_out()
        cluster_centers = self.kmeans.cluster_centers_

        self.top_words_per_cluster = {}
        for i in range(self.n_clusters):
            # Ambil indeks kata-kata dengan nilai TF-IDF tertinggi di klaster
            top_indices = np.argsort(cluster_centers[i])[-3:][::-1]
            self.top_words_per_cluster[i] = [terms[idx] for idx in top_indices]

        for cluster, words in self.top_words_per_cluster.items():
            print(f"Klaster {cluster}: {', '.join(words)}")
        
        self.next(self.save_results)

    @step
    def save_results(self):
        """Simpan hasil klastering ke file CSV."""
        self.data.to_csv(self.output_csv, index=False)
        print(f"Hasil klaster disimpan ke {self.output_csv}.")
        self.next(self.end)

    @step
    def end(self):
        """Akhiri flow."""
        print("Flow selesai.")

if __name__ == '__main__':
    WhatsAppClusteringFlow()

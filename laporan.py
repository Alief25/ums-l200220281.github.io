import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from dominate.tags import *
from dominate import document

def main():
    # Langkah 1: Muat Data
    df = pd.read_csv('data_group.csv')
    documents = df['Message'].values.astype("U")

    # Langkah 2: TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(documents)

    # Langkah 3 & 4: K-Means Clustering 
    cluster_results = {}
    for k in range(2, 6):
        kmeans_model = KMeans(n_clusters=k, random_state=42)
        labels = kmeans_model.fit_predict(X)
        cluster_results[k] = {
            'model': kmeans_model,
            'labels': labels,
        }

    # Langkah 5: Generate HTML dengan background gambar dan penjelasan
    doc = document(title='Clustering Report')

    with doc.head:
        link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css')
        style("""
            body {
                background-image: url('bg.jpg');
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
                color: white;
                text-align: center;
            }
            .container {
                background-color: rgba(0, 0, 0, 0.8);
                padding: 20px;
                border-radius: 10px;
                margin-top: 50px;
            }
            .nama-nim {
                font-size: 1.5em;
                font-weight: bold;
            }
            .img-fluid {
                max-width: 65%;
                height: auto;
                display: block;
                margin-left: auto;
                margin-right: auto;
            }
            .back-button {
                position: absolute;
                top: 20px;
                right: 20px;
            }
        """)

    with doc:
        with div(cls='container'):
            h1('Laporan Hasil Clustering')
            p("Nama: Muhammad Alief Adhitya Pratama", cls='nama-nim')
            p("NIM: L200220281", cls='nama-nim')

            # Penjelasan Langkah-langkah dengan tempat gambar
            h2('Penjelasan Langkah-langkah')
            with ul():
                with li():
                    p("Langkah 1: Data dimuat dari file txt yang berisi pesan.")
                    img(src='gambar1.png', alt='Gambar Langkah 1', cls='img-fluid')
                with li():
                    p("Langkah 2: Data diproses menggunakan TF-IDF untuk merepresentasikan pesan dalam bentuk numerik.")
                    img(src='gambar2.png', alt='Gambar Langkah 2', cls='img-fluid')
                with li():
                    p("Langkah 3 & 4: Data dikelompokkan menggunakan algoritma K-Means dengan berbagai jumlah cluster.")
                    img(src='gambar3.png', alt='Gambar Langkah 3 & 4', cls='img-fluid')
                with li():
                    p("Langkah 5: Hasil clustering ditampilkan dalam laporan HTML.")

            # Hasil Clustering
            for k, result in cluster_results.items():
                h2(f'Hasil Klustering untuk {k} Cluster')
                with table(cls='table table-striped text-light'):
                    with thead():
                        with tr():
                            th('Kluster')
                            th('Kata yang sering muncul')

                    with tbody():
                        for i in range(k):
                            cluster_indices = (result['labels'] == i)
                            cluster_texts = X[cluster_indices.nonzero()[0]]
                            mean_tfidf = cluster_texts.mean(axis=0).A1
                            top_indices = mean_tfidf.argsort()[-3:][::-1]
                            top_words = [vectorizer.get_feature_names_out()[index] for index in top_indices]

                            with tr():
                                td(f'{i + 1}')
                                td(', '.join(top_words))

        # Tombol kembali di pojok kanan atas
        with a("Kembali ke Halaman Utama", href="index.html", cls="btn btn-primary back-button"):
            pass

    # Simpan laporan HTML
    with open('laporan.html', 'w', encoding='utf-8') as f:
        f.write(doc.render())

    print("Laporan HTML telah disimpan ke 'laporan.html'")

if __name__ == '__main__':
    main()

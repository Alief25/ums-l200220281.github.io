import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
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
    cluster_results = {}  # Inisialisasi cluster_results 
    
    for k in range(2, 6):  # Contoh: Clustering untuk k=2, 3, 4, 5
        kmeans_model = KMeans(n_clusters=k, random_state=42)
        labels = kmeans_model.fit_predict(X)
        
        # Simpan hasil ke cluster_results (tanpa Silhouette Score)
        cluster_results[k] = {
            'model': kmeans_model,
            'labels': labels,
        }

    # Langkah 5: Analisis Hasil dan Generate HTML
    doc = document(title='Clustering Report')

    with doc.head:
        link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css')
        style("""
            body {
                background-image: url('bg.jpg');
                background-size: cover; 
                background-repeat: no-repeat; 
            }
            .nama-nim { /* Tambahkan class untuk nama dan nim */
                font-size: 1.5em; /* Ubah ukuran font */
                font-weight: bold;/* Ubah font weight */
            }
        """) 

    with doc:
        with div(cls='container'):
            h1('Laporan Hasil')
            # Menambahkan Nama dan NIM dengan class "nama-nim"
            p(f"Nama: Muhammad Alief Adhitya Pratama", cls='nama-nim')  
            p(f"NIM: L200220281", cls='nama-nim') 
            
            for k, result in cluster_results.items():
                h2(f'hasil dari kluster ke {k} ')  
                # Silhouette Score dihapus
                
                with table(cls='table table-striped'):
                    with thead():
                        with tr():
                            th('Kluster')
                            th('Kata yang sering muncul')

                    with tbody():
                        all_top_words = set()
                        for i in range(k):
                            cluster_indices = (result['labels'] == i)
                            cluster_texts = X[cluster_indices.nonzero()[0]]
                            mean_tfidf = cluster_texts.mean(axis=0).A1

                            sorted_indices = mean_tfidf.argsort()[::-1]
                            top_indices = []
                            for index in sorted_indices:
                                word = vectorizer.get_feature_names_out()[index]
                                if word not in all_top_words:
                                    top_indices.append(index)
                                    all_top_words.add(word)
                                    if len(top_indices) == 3:
                                        break

                            top_words = [vectorizer.get_feature_names_out()[index] for index in top_indices]
                            
                            with tr():
                                td(f'{i + 1}')
                                td(', '.join(top_words))

    # Simpan laporan HTML
    with open('laporan.html', 'w', encoding='utf-8') as f:
        f.write(doc.render())

    print("Laporan HTML telah disimpan ke 'laporan.html'")

if __name__ == '__main__':
    main()
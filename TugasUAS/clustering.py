import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np  # Import numpy untuk operasi array

def main():
    # Langkah 1: Baca data CSV
    data = pd.read_csv('data_group.csv')

    # Langkah 2: Ekstrak pesan (message)
    texts = data['Message'].dropna()  # Menggunakan 'Message' untuk mengakses kolom

    # Langkah 3: TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X = vectorizer.fit_transform(texts)

    # Langkah 4: KMeans Clustering dengan berbagai jumlah cluster
    cluster_counts = [3, 4, 5]
    cluster_results = {}

    for k in cluster_counts:
        kmeans = KMeans(n_clusters=k, random_state=42)
        labels = kmeans.fit_predict(X)
        silhouette_avg = silhouette_score(X, labels)
        cluster_results[k] = {'model': kmeans, 'labels': labels, 'silhouette_score': silhouette_avg}

        print(f"Silhouette Score for {k} clusters: {silhouette_avg:.4f}")

    # Langkah 5: Analisis Hasil
    for k, result in cluster_results.items():
        print(f"\nTop words in {k}-clusters:")
        kmeans_model = result['model']
        labels = np.array(result['labels'])  # Konversi labels ke array NumPy
        for i in range(k):
            # Ambil indeks dokumen yang termasuk dalam cluster i
            cluster_indices = (labels == i)
            cluster_texts = X[cluster_indices.nonzero()[0]]  # Ambil dokumen yang cocok
            # Rata-rata nilai TF-IDF per fitur untuk cluster ini
            mean_tfidf = cluster_texts.mean(axis=0).A1
            # Ambil indeks dari nilai TF-IDF tertinggi
            top_indices = mean_tfidf.argsort()[-3:][::-1]
            # Ekstrak kata-kata dengan nilai TF-IDF tertinggi
            top_words = [vectorizer.get_feature_names_out()[index] for index in top_indices]
            print(f"Cluster {i + 1}: {', '.join(top_words)}")

    # Langkah 6: Tambahkan hasil clustering ke data asli dan simpan ke CSV
    for k in cluster_counts:
        data[f'cluster_{k}'] = cluster_results[k]['labels']

    data.to_csv('clustered_data.csv', index=False)

if __name__ == '__main__':
    main()
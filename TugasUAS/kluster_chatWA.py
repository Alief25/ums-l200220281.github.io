import pandas as pd
import re

# Memuat file teks
with open('Chat WhatsApp dengan KKI K6 ANJAY.txt', 'r', encoding='utf-8') as file:
    raw_data = file.readlines()

# Fungsi untuk membersihkan teks
def clean_text(text):
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)

# Bersihkan setiap baris
cleaned_data = [clean_text(line) for line in raw_data]

# Simpan hasil ke dalam file CSV
df = pd.DataFrame(cleaned_data, columns=['Message'])
df.to_csv('data_group.csv', index=False)
print("Data cleaned and saved to 'data_group.csv'")

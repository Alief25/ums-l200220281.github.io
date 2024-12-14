from metaflow import FlowSpec, step

class ProsesKuliahFlow(FlowSpec):

    @step
    def start(self):
        print("=== Proses Kuliah Mahasiswa ===\n")
        self.output = "<h1>Proses Kuliah Mahasiswa</h1>\n"
        self.output += "<p><strong>Langkah 1: Pembayaran SPP</strong><br>"
        self.output += "Mahasiswa harus membayar SPP terlebih dahulu untuk dapat mengikuti perkuliahan.<br>"
        self.output += "Setelah pembayaran SPP dilakukan, mahasiswa akan mendapatkan akses untuk mengambil mata kuliah.</p>\n"
        self.next(self.ambil_mata_kuliah)
    
    @step
    def ambil_mata_kuliah(self):
        self.output += "<p><strong>Langkah 2: Mengambil Mata Kuliah</strong><br>"
        self.output += "Mahasiswa dapat memilih mata kuliah yang ingin diambil dan mendapatkan konfirmasi.</p>\n"
        self.next(self.ikut_kuliah)

    @step
    def ikut_kuliah(self):
        self.output += "<p><strong>Langkah 3: Mengikuti Perkuliahan</strong><br>"
        self.output += "Mahasiswa mengikuti perkuliahan sesuai jadwal dan mendapatkan materi dari dosen.</p>\n"
        self.next(self.input_nilai)

    @step
    def input_nilai(self):
        self.output += "<p><strong>Langkah 4: Menginput Nilai</strong><br>"
        self.output += "Dosen memberikan nilai, dan mahasiswa menginput nilai untuk mata kuliah tersebut.</p>\n"
        self.next(self.nilai_akhir)

    @step
    def nilai_akhir(self):
        self.output += "<p><strong>Langkah 5: Mendapatkan Nilai Akhir</strong><br>"
        self.output += "Mahasiswa melihat nilai akhir yang akan menjadi bagian dari transkrip akademik.</p>\n"
        self.next(self.end)

    @step
    def end(self):
        self.output += "<h2>Proses Kuliah Telah Selesai.</h2>"
        print("Output disimpan ke file output.html.")
        # Simpan output ke file HTML
        with open("output.html", "w") as f:
            f.write(self.output)

if __name__ == '__main__':
    ProsesKuliahFlow()
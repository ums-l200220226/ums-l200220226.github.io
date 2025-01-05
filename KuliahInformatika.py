from metaflow import FlowSpec, step

class KuliahFlow(FlowSpec):
    @step
    def start(self):
        print("Memulai proses mengikuti kuliah di program Informatika.")
        self.next(self.bayar_spp)

    @step
    def bayar_spp(self):
        print("Mahasiswa melakukan pembayaran SPP untuk semester ini.")
        self.next(self.registrasi_kuliah)

    @step
    def registrasi_kuliah(self):
        print("Mahasiswa melakukan registrasi mata kuliah.")
        self.next(self.mengikuti_kuliah)

    @step
    def mengikuti_kuliah(self):
        print("Mahasiswa aktif mengikuti perkuliahan.")
        self.next(self.mengerjakan_tugas)

    @step
    def mengerjakan_tugas(self):
        print("Mahasiswa mengerjakan tugas-tugas dari dosen.")
        self.next(self.mengerjakan_ujian)

    @step
    def mengerjakan_ujian(self):
        print("Mahasiswa mengikuti ujian tengah semester dan ujian akhir semester.")
        self.next(self.mendapatkan_nilai)

    @step
    def mendapatkan_nilai(self):
        print("Mahasiswa mendapatkan nilai akhir mata kuliah.")
        self.next(self.end)

    @step
    def end(self):
        print("Proses perkuliahan selesai. Mahasiswa berhasil menyelesaikan semester.")

if __name__ == "__main__":
    KuliahFlow()
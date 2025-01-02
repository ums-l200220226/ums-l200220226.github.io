from metaflow import FlowSpec, step

class SemesterFlow(FlowSpec):
    """A flow that simulates the process of a university semester in the Informatics program."""

    @step
    def start(self):
        print("Memulai perjalanan semester di program Informatika.")
        self.next(self.registrasi_matakuliah)

    @step
    def registrasi_matakuliah(self):
        """Step untuk registrasi matakuliah awal semester."""
        print("Mahasiswa melakukan registrasi matakuliah untuk semester ini.")
        self.next(self.pembayaran)

    @step
    def pembayaran(self):
        """Step untuk proses pembayaran semester."""
        print("Mahasiswa melakukan pembayaran semester.")
        self.next(self.perencanaan_studi)

    @step
    def perencanaan_studi(self):
        """Step untuk merencanakan dan mengisi KRS."""
        print("Mahasiswa merencanakan studi dan mengisi KRS.")
        self.next(self.kehadiran_kuliah)

    @step
    def kehadiran_kuliah(self):
        """Step untuk mengikuti kuliah tatap muka atau daring."""
        print("Mahasiswa mengikuti kuliah.")
        self.next(self.mengerjakan_ujian)

    @step
    def mengerjakan_ujian(self):
        """Step untuk mengikuti ujian tengah semester dan akhir semester."""
        print("Mahasiswa mengerjakan ujian akhir semester.")
        self.next(self.mendapatkan_nilai)

    @step
    def mendapatkan_nilai(self):
        """Step untuk mendapatkan hasil nilai dari ujian semester."""
        print("Mahasiswa mendapatkan nilai ujian dan KHS.")
        self.next(self.akhir_semester)

    @step
    def akhir_semester(self):
        """Step akhir yang menandakan semester selesai."""
        print("Semester selesai, mahasiswa berhasil melewati proses akademik.")
        self.next(self.end)

    @step
    def end(self):
        """This is the 'end' step. All flows must have an 'end' step, which is the last step in the flow."""
        print("Proses akademik semester selesai.")
        
if __name__ == "__main__":
    SemesterFlow()

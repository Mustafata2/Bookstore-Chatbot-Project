import pandas as pd



veriler = [
    {"Kitap Adi": "Harry Potter ve Felsefe Taşı", "Yazar": "J.K. Rowling", "Tur": "Fantastik", "Fiyat": 350, "Stok": "Var"},
    {"Kitap Adi": "Harry Potter ve Sırlar Odası", "Yazar": "J.K. Rowling", "Tur": "Fantastik", "Fiyat": 360, "Stok": "Yok"},
    {"Kitap Adi": "Yüzüklerin Efendisi", "Yazar": "Tolkien", "Tur": "Fantastik", "Fiyat": 450, "Stok": "Var"},
    {"Kitap Adi": "Hobbit", "Yazar": "Tolkien", "Tur": "Fantastik", "Fiyat": 200, "Stok": "Var"},
    {"Kitap Adi": "Taht Oyunları", "Yazar": "George R.R. Martin", "Tur": "Fantastik", "Fiyat": 420, "Stok": "Var"},
    {"Kitap Adi": "Yerdeniz Büyücüsü", "Yazar": "Ursula K. Le Guin", "Tur": "Fantastik", "Fiyat": 180, "Stok": "Var"},

    {"Kitap Adi": "Dune", "Yazar": "Frank Herbert", "Tur": "Bilim Kurgu", "Fiyat": 400, "Stok": "Var"},
    {"Kitap Adi": "1984", "Yazar": "George Orwell", "Tur": "Bilim Kurgu", "Fiyat": 180, "Stok": "Var"},
    {"Kitap Adi": "Fahrenheit 451", "Yazar": "Ray Bradbury", "Tur": "Bilim Kurgu", "Fiyat": 160, "Stok": "Var"},
    {"Kitap Adi": "Cesur Yeni Dünya", "Yazar": "Aldous Huxley", "Tur": "Bilim Kurgu", "Fiyat": 190, "Stok": "Var"},
    {"Kitap Adi": "Otostopçunun Galaksi Rehberi", "Yazar": "Douglas Adams", "Tur": "Bilim Kurgu", "Fiyat": 140, "Stok": "Var"},
    {"Kitap Adi": "Vakıf", "Yazar": "Isaac Asimov", "Tur": "Bilim Kurgu", "Fiyat": 210, "Stok": "Var"},
    {"Kitap Adi": "Ben, Robot", "Yazar": "Isaac Asimov", "Tur": "Bilim Kurgu", "Fiyat": 170, "Stok": "Var"},

    {"Kitap Adi": "Sherlock Holmes: Akıl Oyunları", "Yazar": "Arthur Conan Doyle", "Tur": "Polisiye", "Fiyat": 150, "Stok": "Var"},
    {"Kitap Adi": "Doğu Ekspresinde Cinayet", "Yazar": "Agatha Christie", "Tur": "Polisiye", "Fiyat": 160, "Stok": "Var"},
    {"Kitap Adi": "On Kişiydiler", "Yazar": "Agatha Christie", "Tur": "Polisiye", "Fiyat": 155, "Stok": "Yok"},
    {"Kitap Adi": "İstanbul Hatırası", "Yazar": "Ahmet Ümit", "Tur": "Polisiye", "Fiyat": 220, "Stok": "Var"},
    {"Kitap Adi": "Beyoğlu Rapsodisi", "Yazar": "Ahmet Ümit", "Tur": "Polisiye", "Fiyat": 210, "Stok": "Var"},
    {"Kitap Adi": "Kırlangıç Çığlığı", "Yazar": "Ahmet Ümit", "Tur": "Polisiye", "Fiyat": 200, "Stok": "Var"},
    {"Kitap Adi": "Da Vinci Şifresi", "Yazar": "Dan Brown", "Tur": "Polisiye", "Fiyat": 230, "Stok": "Var"},


    {"Kitap Adi": "Nutuk", "Yazar": "Atatürk", "Tur": "Tarih", "Fiyat": 300, "Stok": "Var"},
    {"Kitap Adi": "Şu Çılgın Türkler", "Yazar": "Turgut Özakman", "Tur": "Tarih", "Fiyat": 220, "Stok": "Var"},
    {"Kitap Adi": "Bir Ömür Nasıl Yaşanır?", "Yazar": "İlber Ortaylı", "Tur": "Tarih", "Fiyat": 180, "Stok": "Var"},
    {"Kitap Adi": "Osmanlı Tarihi", "Yazar": "Halil İnalcık", "Tur": "Tarih", "Fiyat": 250, "Stok": "Var"},
    {"Kitap Adi": "Sapiens", "Yazar": "Yuval Noah Harari", "Tur": "Tarih", "Fiyat": 240, "Stok": "Var"},

    {"Kitap Adi": "Böyle Buyurdu Zerdüşt", "Yazar": "Friedrich Nietzsche", "Tur": "Felsefe", "Fiyat": 140, "Stok": "Var"},
    {"Kitap Adi": "Sofie'nin Dünyası", "Yazar": "Jostein Gaarder", "Tur": "Felsefe", "Fiyat": 210, "Stok": "Var"},
    {"Kitap Adi": "Devlet", "Yazar": "Platon", "Tur": "Felsefe", "Fiyat": 120, "Stok": "Var"},
    {"Kitap Adi": "Simyacı", "Yazar": "Paulo Coelho", "Tur": "Felsefe", "Fiyat": 150, "Stok": "Var"},
    {"Kitap Adi": "Denemeler", "Yazar": "Montaigne", "Tur": "Felsefe", "Fiyat": 130, "Stok": "Var"},

    {"Kitap Adi": "Atomik Alışkanlıklar", "Yazar": "James Clear", "Tur": "Kişisel Gelişim", "Fiyat": 190, "Stok": "Var"},
    {"Kitap Adi": "İktidar", "Yazar": "Robert Greene", "Tur": "Kişisel Gelişim", "Fiyat": 250, "Stok": "Var"},
    {"Kitap Adi": "Dost Kazanma Sanatı", "Yazar": "Dale Carnegie", "Tur": "Kişisel Gelişim", "Fiyat": 160, "Stok": "Var"},
    {"Kitap Adi": "Zengin Baba Yoksul Baba", "Yazar": "Robert Kiyosaki", "Tur": "Kişisel Gelişim", "Fiyat": 180, "Stok": "Var"},

    {"Kitap Adi": "Küçük Prens", "Yazar": "Antoine de Saint-Exupéry", "Tur": "Çocuk", "Fiyat": 90, "Stok": "Var"},
    {"Kitap Adi": "Şeker Portakalı", "Yazar": "Jose Mauro de Vasconcelos", "Tur": "Çocuk", "Fiyat": 110, "Stok": "Var"},
    {"Kitap Adi": "Charlie'nin Çikolata Fabrikası", "Yazar": "Roald Dahl", "Tur": "Çocuk", "Fiyat": 120, "Stok": "Var"},
    {"Kitap Adi": "Alice Harikalar Diyarında", "Yazar": "Lewis Carroll", "Tur": "Çocuk", "Fiyat": 100, "Stok": "Var"},

    {"Kitap Adi": "Suç ve Ceza", "Yazar": "Dostoyevski", "Tur": "Roman", "Fiyat": 220, "Stok": "Var"},
    {"Kitap Adi": "Sefiller", "Yazar": "Victor Hugo", "Tur": "Roman", "Fiyat": 280, "Stok": "Var"},
    {"Kitap Adi": "Kürk Mantolu Madonna", "Yazar": "Sabahattin Ali", "Tur": "Roman", "Fiyat": 120, "Stok": "Var"},
    {"Kitap Adi": "Saatleri Ayarlama Enstitüsü", "Yazar": "Ahmet Hamdi Tanpınar", "Tur": "Roman", "Fiyat": 200, "Stok": "Var"},
    {"Kitap Adi": "Tutunamayanlar", "Yazar": "Oğuz Atay", "Tur": "Roman", "Fiyat": 280, "Stok": "Var"},
    {"Kitap Adi": "Masumiyet Müzesi", "Yazar": "Orhan Pamuk", "Tur": "Roman", "Fiyat": 260, "Stok": "Var"},
    {"Kitap Adi": "Anna Karenina", "Yazar": "Tolstoy", "Tur": "Roman", "Fiyat": 250, "Stok": "Yok"},
    {"Kitap Adi": "Dönüşüm", "Yazar": "Franz Kafka", "Tur": "Roman", "Fiyat": 80, "Stok": "Var"},
    {"Kitap Adi": "İnce Memed", "Yazar": "Yaşar Kemal", "Tur": "Roman", "Fiyat": 250, "Stok": "Var"}
]

df = pd.DataFrame(veriler)
df.to_excel("kitap_envanteri.xlsx", index=False)

print(f"✅ ENVANTER GÜNCELLENDİ! Toplam {len(df)} kitap, 8 farklı kategoriye ayrıldı.")
print("Kategoriler: Roman, Bilim Kurgu, Tarih, Felsefe, Çocuk, Kişisel Gelişim, Polisiye, Fantastik")
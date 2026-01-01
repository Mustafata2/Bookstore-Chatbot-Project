import pandas as pd
import random
import string
import os

templates = {
    "greeting": [ 
        "Merhaba", "Selam", "Günaydın", "İyi günler", "Selamlar bot", 
        "Tünaydın", "Selamun aleyküm", "Merhabalar", "Slm",
        "İyi akşamlar", "Kolay gelsin", "Naber", "Hey", "Orada mısın?", 
        "Huu", "Ses ver", "Uyuyor musun?", "Dükkan açık mı?", "Selam millet"
    ],
    "goodbye": [ 
        "Görüşürüz", "Hoşçakal", "Bay bay", "Kib", "Bye", "Kaçtım ben",
        "İyi çalışmalar", "Allah'a emanet",
        "Güle güle", "Sonra görüşürüz", "Çıkış yapıyorum", "Kapatıyorum", 
        "Hadi ben kaçar", "Müsadenle", "Sohbeti bitir", "Ben kaçtım"
    ],
    "ask_price": [ 
        "{kitap} kaç para?", "{kitap} fiyatı nedir?", "{kitap} ne kadar?",
        "Bu kitabın fiyatını öğrenebilir miyim?", "{kitap} pahalı mı?",
        "{kitap} indirimli fiyatı ne?", "Kaç TL {kitap}?",
        "{kitap} ücreti ne?", "{kitap} kaça olur?", "{kitap} etiketi ne?", 
        "Buna ne kadar vericem: {kitap}", "Cebimde 100 lira var {kitap} yeter mi?", 
        "{kitap} ederi nedir?", "Fiyat bilgisi alabilir miyim {kitap} için?",
        "{kitap} kaça patlar?", "{kitap} için cüzdanımdan ne çıkar?"
    ],
    "ask_stock": [ 
        "{kitap} var mı?", "Elinizde {kitap} kaldı mı?", "{kitap} stokta mı?",
        "{kitap} tükendi mi?", "Mağazada {kitap} bulabilir miyim?",
        "{kitap} getirebilir misiniz?",
        "{kitap} ne zaman gelir?", "Depoda {kitap} var mı?", "Rafta {kitap} duruyor mu?", 
        "Aradığım kitap {kitap}, sizde bulunur mu?", "{kitap} satıyor musunuz?",
        "{kitap} kitabı mevcut mu?", "Baskısı var mı {kitap}?"
    ],
    "add_to_cart": [ 
        "{kitap} sepete ekle", "{kitap} alıcam", "Sepetime {kitap} at",
        "{kitap} siparişi ver", "{kitap} satın al",
        "{kitap} ödeme yapcam", "{kitap} kitabından 1 adet istiyorum", 
        "Sepete {kitap} koyar mısın?", "Bunu alıyorum: {kitap}", "{kitap} ödemesini yapayım"
    ],
    "return_product": [
        "İade etmek istiyorum", "Siparişimi iptal et", "Geri vermek istiyorum",
        "Bu ürünü iade edebilir miyim?", "İade kodu oluştur",
        "Jelatini açtım iade olur mu?", "Paket yırtıldı geri alır mısınız?",
        "Kargo ücretini kim ödüyor?", "Hasarlı geldi kitap", "Yanlış ürün geldi", 
        "Param ne zaman yatar?", "Beğenmedim geri yollayacağım"
    ],
    "ask_category": [
        "Bana {kategori} öner", "En iyi {kategori} kitapları",
        "{kategori} türünde ne var?", "Yeni {kategori} romanları",
        "{kategori} okumak istiyorum", "Sadece {kategori} olsun",
        "{kategori} rafı nerede?", "Popüler {kategori} listesi",
        "Canım {kategori} çekiyor", "{kategori} bölümüne bakabilir miyim?",
        "Bana {kategori} türündeki kitapları öner", "{kategori} kitapları",
        "{kategori} türündeki kitapları listele", "{kategori} kitapları nelerdir?",
        "{kategori} kitaplarını listele"
    ],
    "surprise_recommendation": [ 
        "Bana sürpriz bir kitap öner", "Ne okusam bilmiyorum",
        "Rastgele bir kitap seç", "Bugün şansıma hangi kitap var?",
        "Kararsız kaldım sen seç", "Bana güzel bir kitap bul", 
        "Hediye alacağım ne önerirsin?", "Beni şaşırt"
    ]
}

def lowercase_randomly(text):
    if random.random() < 0.5: return text.lower()
    return text

def add_filler_words(text):
    prefixes = ["Hocam", "Reis", "Acaba", "Şey", "Bi baksana", "Selam", "Pardon"]
    if random.random() < 0.25: text = f"{random.choice(prefixes)} {text}"
    return text

def add_typo(text):
    if random.random() > 0.3: return text
    char_list = list(text)
    if len(char_list) < 4: return text
    idx = random.randint(1, len(char_list) - 1)
    if random.random() > 0.5: char_list[idx] = random.choice(string.ascii_lowercase)
    else: del char_list[idx]
    return "".join(char_list)


data_list = []

for intent, sentence_list in templates.items():

    for _ in range(600):
        tmpl = random.choice(sentence_list)
        
        text = tmpl
        if "{kitap}" in text: text = text.format(kitap="PH_KITAP")
        elif "{yazar}" in text: text = text.format(yazar="PH_YAZAR")
        elif "{kategori}" in text: text = text.format(kategori="PH_KATEGORI")
        

        text = lowercase_randomly(text)
        text = add_filler_words(text)
        text = add_typo(text)
        
        data_list.append({"text": text, "intent": intent})


df = pd.DataFrame(data_list)
df = df.drop_duplicates(subset=['text'])
df = df.sample(frac=1).reset_index(drop=True)


os.makedirs("data", exist_ok=True)
output_file = "data/chatbot_dataset_final_production.xlsx"
df.to_excel(output_file, index=False)

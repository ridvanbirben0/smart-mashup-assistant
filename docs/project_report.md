# Proje Raporu: Uçtan Uca Yapay Zekâ ile Smart Mashup Assistant

**Hazırlayan:** Rıdvan Efe Birben — Dokuz Eylül Üniversitesi, Elektrik-Elektronik Mühendisliği  
**Proje Adı:** Smart Mashup Assistant (Frekanslardan Ton Tahmini ve Akıllı DJ Asistanı)

---

## 1. Problem Tanımı
Elektronik müzik prodüksiyonunda ve DJ performanslarında, parçalar arası kusursuz geçiş (mashup/mix) yapabilmek için ritim (BPM) ve harmonik ton (Key) uyumu kritik öneme sahiptir. Canlı performans (sahne) sırasında binlerce şarkılık devasa arşivler içinden o an çalınan parçaya en uygun sıradaki şarkıyı seçmek ciddi bir zaman ve odak kaybı yaratmaktadır. Bu projenin amacı, ses dosyalarının dijital sinyal işleme (DSP) metriklerinden (Chroma frekansları) yola çıkarak şarkıların tonunu makine öğrenmesi ile tahmin eden ve DJ'e anında BPM/Ton uyumlu şarkı öneren akıllı bir karar destek sistemi geliştirmektir.

---

## 2. Veri Toplama ve Hazırlama
Projede yaklaşık 7.500 satırlık elektronik müzik veri seti kullanılmıştır. Veri bilimi etiği, şeffaflık ve projenin tekrarlanabilirliği (reproducibility) ilkeleri doğrultusunda, ham veri seti Kaggle platformundan ([House Music DJ Library - Kaggle](https://www.kaggle.com/datasets/enesayata/house-music-dj-library-key-bpm-and-chroma)) temin edilerek Pandas kütüphanesi ile çalışma ortamına aktarılmıştır.

* **Veri Temizliği ve Optimizasyon:** Yapay zeka modelinin "veri sızıntısı (data leakage)" yaşamasını ve ezber yapmasını önlemek adına, hedef değişkenle aynı sonucu veren alternatif algoritma çıktıları (`harmoniq_key`, `harmoniq_key_camelot` vb.) eğitim setinden ($X$) izole edilmiştir. Aynı şekilde, modelin matematiksel olarak işleyemeyeceği metin tabanlı sütunlar (`artist`, `title`, `track_id`) denklemden çıkarılarak veri seti makine öğrenmesine uygun, pürüzsüz bir sayısal matris haline getirilmiştir.
* **Keşifsel Veri Analizi (EDA):** Veri seti üzerinde Matplotlib kullanılarak yapılan görselleştirmelerde, elektronik müzik arşivinin büyük bir kısmının 124–125 BPM bandında yoğunlaştığı ve Camelot Wheel sisteminde Minör tonların endüstri standardı olarak domine ettiği tespit edilmiştir. Hedef değişken ($y$) olarak, sektördeki en yüksek tahmin doğruluğuna sahip olan `mik_key_camelot` (Mixed In Key) sütunu referans alınmıştır.

---

## 3. Model Kurma ve Eğitme
Problemin bir "Sınıflandırma (Classification)" problemi olması ve ses frekanslarının belirli eşik değerleriyle (threshold) karakterize edilmesi nedeniyle, şeffaf mantık kapılarıyla çalışan **Decision Tree Classifier (Karar Ağacı Sınıflandırıcısı)** algoritması tercih edilmiştir. Veri seti, ezberlemenin (overfitting) önüne geçmek için %80 Eğitim (Train) ve %20 Test (Test) olarak `train_test_split` ile ayrılmış, tekrarlanabilirlik için `random_state=42` parametresiyle sabitlenerek eğitilmiştir.

---

## 4. Tahmin ve Değerlendirme (Sonuçlar)
Model, hiç görmediği 1.514 test şarkısı üzerinde **%79.79** oranında genel doğruluk (accuracy) skoruna ulaşmıştır.

* **Müzikal Zekâ ve Çıkarım:** Modelin yaptığı hatalar incelendiğinde, tahminlerin rastgele uydurulmuş değerler olmadığı görülmüştür. Örneğin; gerçek tonu 5A (Do Minör) olan bir parça için modelin tahmini 6A (Sol Minör) olmuştur. Camelot Wheel üzerinde yan yana duran ve ortak notalara sahip bu "komşu tonların" karıştırılması, algoritmanın frekanslar arası müzikal ilişkiyi ezberlemediğini, aksine matematiksel olarak kavradığını kanıtlamaktadır.

---

## 5. Nihai Çıktı ve Gelecek Vizyonu (Genişletilmiş Versiyon)
Eğitilen modelin üzerine inşa edilen **Smart Mashup Assistant**, terminal üzerinden sonsuz döngüyle çalışan interaktif bir Python fonksiyonuna dönüştürülmüştür. DJ'den anlık olarak BPM ve Ton bilgisini alıp, $\pm 3\text{ BPM}$ esneklik toleransıyla kütüphanedeki en uygun 5 parçayı saniyeler içinde ekrana sunmaktadır. Projenin gelecekteki ölçeklendirme hedefleri şunlardır:

1. **Model Yükseltmesi:** Karar Ağacı mimarisinin Random Forest (Rastgele Orman) algoritmasına geçirilerek komşu ton sapmalarının minimize edilmesi.
2. **Doğrudan Ses Dalgaları Analizi (TuneBat Entegrasyonu):** Sisteme doğrudan bir `.wav` veya `.mp3` dosyası yüklendiğinde, ses dalgalarının (waveform) transient ve chroma özelliklerini analiz edip, BPM ve Ton metriklerini kendiliğinden çıkararak kütüphaneye otomatik kaydeden bir modül geliştirilmesi.
3. **Audio Fingerprinting (Shazam Benzeri Tanıma):** Canlı dinletilen bir ses sinyalini mikrofondan yakalayıp analiz eden, parçayı veri tabanına işleyen ve kullanıcı etkileşimiyle durmadan büyüyen, otonom bir müzik ekosistemi (Machine Learning Data Flywheel) yaratılması.

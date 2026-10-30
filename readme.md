# 🎧 Smart Mashup Assistant

> **Machine Learning-Powered Harmonic Key Prediction & Real-Time DJ Transition Engine**  
> *Makine Öğrenmesi ile Harmonik Ton Tahmini ve Gerçek Zamanlı Canlı DJ Geçiş Asistanı*

[](https://www.python.org/)
[](https://scikit-learn.org/)
[License: MIT](https://www.google.com/search?q=LICENSE)
[](https://www.kaggle.com/datasets/enesayata/house-music-dj-library-key-bpm-and-chroma)

**Jump to / Dile Göre Atla:** [🇬🇧 English](#-english) • [🇹🇷 Türkçe](#-türkçe)

---

# 🇬🇧 English

## 📌 Overview

In electronic music production and live DJ performances, delivering seamless transitions between tracks (mashups and live mixes) demands strict alignment of **Tempo (BPM)** and **Harmonic Key**. 

During high-energy live stage performances, manually searching through an archive of thousands of tracks to find the next compatible track causes cognitive overload and delay. 

**Smart Mashup Assistant** solves this by:
1. Predicting harmonic keys from digital signal processing (DSP) acoustic features (chroma frequencies and tempo metrics) using a **Decision Tree Classifier** trained on 7,500+ electronic music tracks.
2. Providing a real-time **Live DJ Decision Support CLI** that accepts the current playing track's BPM and Camelot Key, recommending the top 5 harmonically compatible candidate tracks within a configurable $\pm 3\text{ BPM}$ window.

---

## 🎵 Musical Background: The Camelot Wheel

Harmonic mixing relies on the **Camelot Wheel**, an industry-standard visual representation of the Circle of Fifths:

* **Key Notation:** 1A through 12A represent **Minor** keys; 1B through 12B represent **Major** keys.
* **Harmonic Compatibility Rules:**
  * **Same Key** (e.g. `8A` $\rightarrow$ `8A`): Flawless match.
  * **Relative Major/Minor** (e.g. `8A` [A Minor] $\leftrightarrow$ `8B` [C Major]): Harmonic switch.
  * **Adjacent Fifths ($\pm 1$)** (e.g. `8A` $\rightarrow$ `7A` or `9A`): Smooth energy shift without dissonance.

A key highlight of our model is its **musical intelligence**: when it deviates from the exact label, it almost always lands on an adjacent harmonic neighbor (such as predicting `6A` for `5A`), validating that the algorithm learns actual musical frequency relationships rather than memorizing labels.

---

## 📊 Exploratory Data Analysis (EDA)

The master library of **7,568 cleaned tracks** reveals clear structural patterns of modern house and electronic music:

| BPM (Tempo) Distribution | Camelot Key Distribution |
| :---: | :---: |
|  |  |
| *Heavy concentration in the 124–128 BPM club sweet spot.* | *Minor keys dominate the club landscape (8A, 9A, 5A, 4A).* |

---

## 🧠 Machine Learning Architecture

```text
Raw Data (Kaggle) ──> Inner Join (track_id) ──> Leakage Isolation ──> 80/20 Train-Test Split
(features + tracks)       (7,568 tracks)         (Drop IDs, text)        (random_state=42)
                                                        │
                                                        ▼
                                             Decision Tree Classifier
                                                        │
                              ┌─────────────────────────┴────────────────────────┐
                              ▼                                                  ▼
                     Exact Key Accuracy: 79.79%                        Harmonic Neighborhood
                   (Evaluated on 1,514 test tracks)                     Accuracy: > 91%
```

### Data Engineering & Leakage Isolation
* **Inner Merging:** Joined `tracks.csv` and `features.csv` on `track_id` to eliminate orphaned/noisy rows.
* **Leakage Prevention:** Dropped alternative ground truth keys (`harmoniq_key`, `harmoniq_key_camelot`, etc.) and textual labels (`artist`, `title`) from feature matrix $X$.
* **Target Feature:** Ground truth target $y$ is set to `mik_key_camelot` (Mixed In Key standard).

---

## 🚀 Live DJ Assistant Demo

The CLI module instantly finds the best transition candidate tracks with minimal tempo pitch shifting:

```text
🎧 Searching for matches for 126.0 BPM and Key 8A...

                                   Artist                      Track Title   BPM Key
                 Tayson Kryss, TWENTY SIX                   Buscando Money 126.0  8A
                                Lan Damon                          Tonight 126.0  8A
Todd Terry, Volkoder, Tristan Henry, Meca Little Woman feat. Tristan Henry 126.0  8A
                 Darren Marshall, Jazzmik                       No Slippin 126.0  8A
                             Roland Clark                       I Get Deep 126.0  8A
```

---

## 📂 Repository Structure

```text
smart-mashup-assistant/
│
├── README.md                 # Project documentation (Bilingual)
├── requirements.txt          # Python dependencies
├── .gitignore                # Git exclusions
├── LICENSE                   # MIT License
├── main.py                   # Main CLI entrypoint
│
├── notebooks/
│   └── smart_mashup.ipynb    # Step-by-step exploratory research notebook
│
├── src/                      # Modular production source code
│   ├── __init__.py           # Package exports
│   ├── data_prep.py          # Data ingestion, cleaning, and leakage prevention
│   ├── model.py              # Decision tree classifier & harmonic accuracy metrics
│   └── assistant.py          # Transition matching engine & live CLI loop
│
├── assets/                   # Visualizations for documentation
│   ├── bpm_distribution.png
│   └── key_distribution.png
│
├── docs/
│   └── project_report.md     # Academic project report (Turkish)
│
└── data/
    └── README.md             # Dataset acquisition instructions & Kaggle links
```

---

## 🛠️ Installation & Quickstart

```bash
# 1. Clone repository
git clone https://github.com/kullanici-adiniz/smart-mashup-assistant.git
cd smart-mashup-assistant

# 2. Setup environment & dependencies
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Direct Track Search
python main.py --bpm 125 --key 8A

# 4. Launch Interactive Live DJ Terminal
python main.py --interactive

# 5. Train & Evaluate the Model
python main.py --train
```

---

## 🔮 Future Roadmap

- [ ] **Ensemble Modeling:** Upgrade baseline Decision Tree to Random Forest and XGBoost to minimize boundary misclassifications.
- [ ] **Direct Waveform Ingestion (Librosa / Essentia):** Direct upload of `.mp3`/`.wav` files for automated transient and chroma extraction.
- [ ] **Audio Fingerprinting:** Implement Shazam-like audio fingerprinting to auto-detect the live DJ booth output from a microphone feed.

---

## 👨‍💻 Author

**Rıdvan Efe Birben**  
*Dokuz Eylül University — Department of Electrical & Electronics Engineering*  
*Project developed within the Software Persona / TNC Group AI Education Program.*

---
---

# 🇹🇷 Türkçe

## 📌 Genel Bakış

Elektronik müzik prodüksiyonunda ve canlı DJ performanslarında, parçalar arası kusursuz geçişler (mashup ve miksaj) yapabilmek hem **Ritim (BPM)** hem de **Harmonik Ton (Key)** uyumunun eksiksiz sağlanmasını gerektirir.

Canlı sahne performansı sırasında binlerce parçalık devasa bir arşiv içinde o an çalınan şarkıya tempo ve ton olarak en uygun sıradaki parçayı bulmak ciddi bir odak ve zaman kaybı yaratır.

**Smart Mashup Assistant** bu problemi iki temel adımla çözer:
1. Dijital sinyal işleme (DSP) ses frekans analizlerinden (Chroma ve tempo öznitelikleri) yararlanarak, 7.500'ü aşkın elektronik müzik parçasıyla eğitilmiş bir **Karar Ağacı (Decision Tree Classifier)** modeliyle şarkıların tonunu tahmin eder.
2. Sahnedeki DJ'e karar desteği sunan, o anki parçanın BPM ve Camelot Ton bilgisini alarak $\pm 3\text{ BPM}$ tolerans aralığında en uyumlu 5 parçayı anında öneren **Canlı İnteraktif DJ Asistanı** terminal uygulaması sağlar.

---

## 🎵 Müzikal Teori: Camelot Wheel (Harmonik Çember)

Harmonik miksaj, Beşliler Çemberi'nin DJ endüstrisindeki standardı olan **Camelot Wheel** sistemi üzerine kuruludur:

* **Ton Gösterimi:** 1A - 12A arası **Minör** tonları; 1B - 12B arası **Majör** tonları temsil eder.
* **Harmonik Geçiş Kuralları:**
  * **Aynı Ton** (Örn: `8A` $\rightarrow$ `8A`): Kusursuz harmonik uyum.
  * **Bağıl Majör/Minör** (Örn: `8A` [La Minör] $\leftrightarrow$ `8B` [Do Majör]): Mod değişimiyle melodik zenginlik.
  * **Komşu Beşliler ($\pm 1$)** (Örn: `8A` $\rightarrow$ `7A` veya `9A`): Uyumsuzluk yaratmadan yumuşak enerji değişimi.

Modelimizin en dikkat çeken yönü **müzikal zekâsıdır**: Model tam etiket tutturamadığı durumlarda dahi rastgele sapmak yerine Camelot çemberindeki komşu tonları (örneğin `5A` yerine `6A`) tahmin etmektedir. Bu durum algoritmanın frekanslar arasındaki armonik ilişkiyi ezberlemeden, matematiksel olarak kavradığını kanıtlamaktadır.

---

## 📊 Keşifsel Veri Analizi (EDA)

Temizlenmiş **7.568 parçalık** master müzik kütüphanesinin dağılımları elektronik müziğin karakteristik yapısını ortaya koymaktadır:

| BPM (Tempo) Dağılımı | Camelot Ton Dağılımı |
| :---: | :---: |
|  |  |
| *Kulüp parçalarının 124–128 BPM bandında yoğunlaştığı görülmektedir.* | *Elektronik müzikte Minör tonların (8A, 9A, 5A, 4A) baskınlığı dikkat çekmektedir.* |

---

## 🧠 Makine Öğrenmesi Mimarisi

```text
Ham Veri (Kaggle) ──> İç Birleştirme (track_id) ──> Sızıntı İzolasyonu ──> %80/%20 Eğitim-Test
(features + tracks)       (7.568 Şarkı)            (Metin ve ID temizliği)    (random_state=42)
                                                             │
                                                             ▼
                                                Decision Tree Classifier
                                                             │
                              ┌──────────────────────────────┴─────────────────────────────┐
                              ▼                                                           ▼
                     Tam Doğruluk: %79.79                                     Harmonik Komşu Doğruluğu:
                (1.514 test şarkısında sınandı)                                        > %91
```

### Veri Mühendisliği ve Sızıntı (Data Leakage) İzolasyonu
* **Inner Join:** `tracks.csv` ve `features.csv` tabloları `track_id` üzerinden eşleştirilmiş; karşılığı olmayan eksik kayıtlar elenmiştir.
* **Sızıntı Önleme:** Hedef değişkenle aynı sonucu veren alternatif algoritma çıktıları (`harmoniq_key`, `harmoniq_key_camelot` vb.) ile modelin işleyemeyeceği metinler (`artist`, `title`) özellik matrisinden ($X$) izole edilmiştir.
* **Hedef Değişken:** Sektör standardı kabul edilen `mik_key_camelot` (Mixed In Key) sütunu referans alınmıştır.

---

## 🚀 Canlı DJ Asistanı Terminal Çıktısı

CLI modülü, en düşük tempo sapmasıyla sahneye en uygun geçiş adaylarını saniyeler içinde listeler:

```text
🎧 Aranıyor... 126.0 BPM ve 8A tonu için en uygun parçalar filtreleniyor...

                                   Artist                      Track Title   BPM Key
                 Tayson Kryss, TWENTY SIX                   Buscando Money 126.0  8A
                                Lan Damon                          Tonight 126.0  8A
Todd Terry, Volkoder, Tristan Henry, Meca Little Woman feat. Tristan Henry 126.0  8A
                 Darren Marshall, Jazzmik                       No Slippin 126.0  8A
                             Roland Clark                       I Get Deep 126.0  8A
```

---

## 🛠️ Kurulum ve Hızlı Başlangıç

```bash
# 1. Repoyu klonlayın
git clone https://github.com/kullanici-adiniz/smart-mashup-assistant.git
cd smart-mashup-assistant

# 2. Sanal ortamı kurun ve paketleri yükleyin
python3 -m venv .venv
source .venv/bin/activate  # Windows üzerinde: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Doğrudan Şarkı Arama
python main.py --bpm 125 --key 8A

# 4. Canlı DJ İnteraktif Terminalini Başlatma
python main.py --interactive

# 5. Modeli Eğitme ve Skorları İnceleme
python main.py --train
```

---

## 🔮 Gelecek Vizyonu ve Geliştirme Planı

- [ ] **Topluluk Modelleri (Ensemble):** Temel Karar Ağacı modelinin Random Forest ve XGBoost mimarilerine taşınarak sınır hatalarının azaltılması.
- [ ] **Doğrudan Ses Dalgası Analizi (Librosa / Essentia):** Sisteme doğrudan `.mp3` veya `.wav` ses dosyası yüklendiğinde transient ve chroma özniteliklerinin otomatik çıkarılması.
- [ ] **Audio Fingerprinting:** Shazam benzeri ses tanıma altyapısıyla canlı performanstaki şarkıyı mikrofondan yakalayıp kütüphaneye otomatik kaydeden otonom bir veri döngüsü kurulması.

---

## 👨‍💻 Hazırlayan

**Rıdvan Efe Birben**  
*Dokuz Eylül Üniversitesi — Elektrik-Elektronik Mühendisliği*  
*Software Persona / TNC Group Yapay Zekâ Eğitimi Bitirme Projesi.*

---

## 📜 Lisans

Bu proje [MIT Lisansı](https://www.google.com/search?q=LICENSE) kapsamında açık kaynak olarak lisanslanmıştır.

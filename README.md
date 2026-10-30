# 🎧 Smart Mashup Assistant

> **Makine Öğrenmesi ile Harmonik Ton Tahmini ve Gerçek Zamanlı Canlı DJ Geçiş Asistanı**

[[https://img.shields.io/badge/python-3.8%2B-blue.svg]](https://www.python.org/)
[[https://img.shields.io/badge/scikit--learn-1.3%2B-orange.svg]](https://scikit-learn.org/)
[[https://img.shields.io/badge/License-MIT-green.svg]](LICENSE)
[[https://img.shields.io/badge/Veri%20Seti-Kaggle-20BEFF.svg]](https://www.kaggle.com/datasets/enesayata/house-music-dj-library-key-bpm-and-chroma)

---

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

Modelimizin en dikkat çeken yönü **müzikal zekâsıdır**: Model tam etiket tutturamadığı durumlarda dahi rastgele sapmak yerine Camelot çemberindeki komşu tonları (örneğin `5A` yerine `6A`) tahmin etmektedir. Bu durum algoritmanın frekanslar arasındaki armonik ilişkiyi ezberlemeden, matematiksel olarak kavradığını gösterir.

---

## 📊 Keşifsel Veri Analizi (EDA)

Temizlenmiş **7.568 parçalık** master müzik kütüphanesinin dağılımları elektronik müziğin karakteristik yapısını ortaya koymaktadır:

| BPM (Tempo) Dağılımı | Camelot Ton Dağılımı |
| :---: | :---: |
| [assets/bpm_distribution.png] | [assets/key_distribution.png] |
| *Kulüp parçalarının 124–128 BPM bandında yoğunlaştığı görülmektedir.* | *Elektronik müzikte Minör tonların (8A, 9A, 5A, 4A) baskınlığı dikkat çekmektedir.* |

---

## 🧠 Makine Öğrenmesi Mimarisi

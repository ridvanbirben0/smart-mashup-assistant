# Dataset Information & Setup Guide

This project leverages acoustic digital signal processing (DSP) features and music metadata to predict harmonic keys and recommend seamless transitions for live DJ mixing.

---

## 📁 Required Data Files

To run the pipeline and interactive assistant, place the following two files into this `data/` folder:

1. `features.csv`: Acoustic and chroma frequency features extracted across 12 semitone chroma bins and tempo markers (73 numerical columns).
2. `tracks.csv`: Metadata for the electronic music library including track ID, artist, title, Mixed In Key annotations (`mik_key_camelot`), and BPM (`mik_bpm`).

---

## 🌐 Dataset Sources

The original dataset is available from the following verified sources:

* **Kaggle:** [House Music DJ Library (Key, BPM, and Chroma)](https://www.kaggle.com/datasets/enesayata/house-music-dj-library-key-bpm-and-chroma)
* **Google Drive Backup:** [Project Data Folder](https://drive.google.com/drive/folders/1PWrezMWxJ7-SAY1aTm2bRMOMOB1OTxmP?usp=sharing)

---

## 🧹 Data Cleaning & Preprocessing Highlights

1. **Inner Merging:** Joined on `track_id` to ensure strictly complete pairs of metadata and audio DSP analyses (filtering out noise/orphaned records).
2. **Leakage Prevention:** Removed alternative algorithmic ground truths (`harmoniq_key`, `harmoniq_key_camelot`, etc.) and textual metadata (`artist`, `title`) from model feature inputs $X$.
3. **Target Standard:** Ground truth target variable $y$ is set to `mik_key_camelot` (Mixed In Key standard).
4. **Final Matrix:** 7,568 tracks $\times$ 73 numerical acoustic features.

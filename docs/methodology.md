# HeatScape Methodology

## 1. Heat

Land Surface Temperature is obtained from Landsat 8/9 Level-2 Surface Temperature.

Temperature(K) = DN × 0.00341802 + 149.0

Temperature(°C) = Temperature(K) - 273.15

The LST values are normalized to 0–100.

---

## 2. Vegetation

NDVI is calculated using Sentinel-2:

NDVI = (B08 - B04) / (B08 + B04)

Higher NDVI indicates greater vegetation.

Vegetation Deficit = 100 - normalized NDVI.

---

## 3. Built-up

ESA WorldCover is used to identify built-up land.

Built-up percentage:

Built-up % =
Built-up pixels / Total pixels × 100

---

## 4. Population

WorldPop population density is normalized to 0–100.

This represents population exposure.

---

## 5. Heat Risk

Heat Risk =

0.45 × Heat
+ 0.25 × Built-up
+ 0.20 × Vegetation Deficit
+ 0.10 × Population Exposure

Risk categories:

0–25: Low
25–50: Moderate
50–75: High
75–100: Critical

The Heat Risk Index is a transparent prototype planning index and is not a validated health-risk prediction.

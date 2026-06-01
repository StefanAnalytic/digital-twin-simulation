<div align="center">

# 🏭 Digital Twin: Discrete Event Simulation (DES)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white&style=for-the-badge)](https://www.python.org/)
[![SimPy](https://img.shields.io/badge/Simulation-SimPy-8A2BE2?style=for-the-badge)](https://simpy.readthedocs.io/)
[![SciPy](https://img.shields.io/badge/Stats-SciPy-%238CAAE6?logo=scipy&logoColor=white&style=for-the-badge)](https://scipy.org/)
[![Dataset](https://img.shields.io/badge/Dataset-AI4I_2020-F7931E?style=for-the-badge)](https://www.kaggle.com/datasets/stephanmatzka/predictive-maintenance-dataset-ai4i-2020)
[![ROI](https://img.shields.io/badge/Net_CapEx_Saved-%2B%E2%82%AC1.95M-emerald?style=for-the-badge&logo=moneygram&logoColor=white)](https://github.com)

**Ein Python-basierter Digital Twin zur CapEx-Optimierung mittels Discrete Event Simulation (DES).**

*Ersetzt naive Excel-Schätzungen durch stochastische Strenge, um betriebliche Engpässe durch intelligente Puffer-Optimierung aufzulösen, anstatt teure und redundante Maschinen zu kaufen.*

---
</div>

## 💰 Business Value & CapEx Impact

Traditionelle Kapazitätsplanung nutzt oft statische Durchschnitte ("Einheiten pro Minute") und ignoriert dabei reale Varianzen, komplexe Warteschlangennetzwerke und kaskadierende Maschinenausfälle völlig. Dieses Modell liefert belastbare, finanzielle Entscheidungsgrundlagen:

<table>
  <tr>
    <td><strong>🚫 Vermiedene CapEx</strong></td>
    <td>Die Simulation beweist mathematisch, dass eine Puffererweiterung für 50.000 € die stochastische Unterversorgung (Starvation) absorbiert und ein <strong>2.000.000 € Maschinen-Investment obsolet macht</strong>.</td>
  </tr>
  <tr>
    <td><strong>💶 Netto CapEx-Ersparnis</strong></td>
    <td>Direkter finanzieller Impact von <strong>1.950.000 €</strong>.</td>
  </tr>
  <tr>
    <td><strong>📈 Throughput Uplift</strong></td>
    <td><strong>+ 1,82%</strong> höherer Durchsatz – isoliert und rein durch Varianzreduktion im System erreicht.</td>
  </tr>
</table>

---

## 🏗️ Operations Research & Technische Architektur

Die Engine hält sich an strikte Best Practices aus dem Bereich Senior Data Science und Operations Research:

| Komponente & OR-Methode | Detail-Logik |
| :--- | :--- |
| **🎲 Stochastische Ausfallmodellierung** | Naive exponentielle Verteilungen reichen für Verschleißteile (Wear-and-Tear) nicht aus. Implementierung einer **Weibull-Verteilung** ($f(x; \lambda, k)$). Shape ($k=1.95$) und Scale ($\lambda=160.81$) Parameter werden dynamisch via Maximum Likelihood Estimation (MLE) direkt aus *Tool Wear* Daten (Kaggle AI4I 2020) gefittet. |
| **🔥 Initialization Bias Handling** | Implementierung von **Welch's Method** (Moving Average Variance) im `TwinTracker`, um den *Steady-State* (eingeschwungenen Zustand) automatisch zu detektieren. Dies schneidet die Warm-up-Phase ab und verhindert statistischen Bias durch eine simulierte leere Fabrik zum Startzeitpunkt ($t=0$). |
| **🛡️ Validation Guard (Reality Check)** | Der `TwinValidator` agiert als harter Gatekeeper. Er erzwingt einen **Two-Sample Kolmogorov-Smirnov-Test ($D_n$)** zwischen simuliertem Durchsatz und historischen ERP-Daten. Der Build schlägt bei einem p-Wert von $p < 0.05$ strikt fehl – so werden CapEx-Entscheidungen auf Basis invalider Modelle technisch verhindert. |

---

## 🚀 Execution & Artifacts

<details>
<summary><b>🛠️ Architektur-Details & Ausführung (Hier klicken zum Aufklappen)</b></summary>

### Code-Struktur
* `src/digital_twin.py`: Beinhaltet die OR-Kernklassen (`TwinTracker`, `TwinValidator`, `ManufacturingTwin`).
* `main.py`: Orchestriert die Simulation, fittet die Weibull-Parameter aus den Kaggle-Daten, führt den KS-Test durch und startet den A/B-Szenariolauf.
* `reports/sim_model_report.md`: Das automatisch generierte Endprodukt – ein detaillierter CapEx-Report als Entscheidungsgrundlage für den CFO.

### Quick Start
```bash
# 1. Abhängigkeiten installieren
pip install -r requirements.txt

# 2. Digital Twin & Simulation ausführen
python main.py

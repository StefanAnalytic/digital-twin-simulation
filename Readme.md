# Digital Twin: Discrete Event Simulation (DES) for CapEx Optimization

## 📌 Project Overview
This repository contains a Python-based **Digital Twin** and **Discrete Event Simulation (DES)** built with `simpy`. It models a stochastic manufacturing environment to optimize CapEx investments. The core objective is to mathematically prove that operational bottlenecks can be resolved via strategic buffer optimization rather than purchasing expensive, redundant machinery.

## 💼 Business Value & Impact
Traditional capacity planning often relies on static averages (e.g., "units per minute"), completely ignoring real-world variance, queueing networks, and cascading machine breakdowns. This model replaces naive Excel estimates with stochastic rigor.
- **CapEx Avoided:** The simulation proves that a 50k € buffer expansion absorbs stochastic starvation, rendering a 2M € new machine investment obsolete.
- **Net CapEx Saved:** 1.950.000 €.
- **Throughput Uplift:** +1.82% isolated purely through variance reduction.

## 🛠️ Technical Architecture & Operations Research
This engine adheres to strict Senior Data Science and Operations Research guidelines:

1. **Stochastic Failure Modeling (MTBF):**
   - Naive exponential failure distributions are inadequate for wear-and-tear components. We implemented a **Weibull Distribution** ($f(x; \lambda, k)$).
   - Shape ($k=1.95$) and Scale ($\lambda=160.81$) parameters are dynamically fitted via Maximum Likelihood Estimation (MLE) directly from real-world *Tool Wear* data using the **Kaggle AI4I 2020 Predictive Maintenance Dataset**.
2. **Initialization Bias Handling (Warm-up):**
   - Implemented **Welch's Method** (Moving Average Variance) within the `TwinTracker` to automatically detect the Steady-State. This truncates the warm-up period, preventing statistical bias caused by an initially empty factory at $t=0$.
3. **Validation Guard (Dirty-ERP Reality):**
   - The `TwinValidator` acts as a hard gatekeeper. It enforces a **Two-Sample Kolmogorov-Smirnov Test ($D_n$)** between the simulated throughput and historical ERP data. 
   - The build is strictly configured to fail if $p < 0.05$, ensuring no CapEx decisions are made on invalid models.

## 🚀 Execution & Artifacts
- `src/digital_twin.py`: Contains the core OR classes (`TwinTracker`, `TwinValidator`, `ManufacturingTwin`).
- `main.py`: Orchestrates the simulation, fits the Weibull parameters from Kaggle data, runs the KS-Test, and executes the A/B scenario.
- `reports/sim_model_report.md`: The auto-generated deliverable detailing the CapEx verdict for the CFO.
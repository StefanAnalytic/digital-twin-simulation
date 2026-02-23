# Digital Twin CapEx Scenario Report

## Stochastics & Initialization
- **Data Source:** Kaggle AI4I 2020 Predictive Maintenance
- **MTBF Model:** Weibull Distribution (MLE Fitted on real Tool Wear)
- **Warm-up Handling:** Welch's Method (Moving Average Variance)
- **Validation Guard:** Two-Sample KS-Test (Passed, $p \ge 0.05$)

## Results: Baseline vs Scenario B
- **Baseline Throughput (Buffer=10):** 3359 units
- **Scenario B Throughput (Buffer=12):** 3420 units
- **Throughput Uplift:** +1.82%

## CapEx Verdict
By investing **50.000 €** to increase the physical buffer space in front of Machine 3 by 20%, we buffer stochastic starvation and breakdown cascades, achieving a 1.82% throughput increase. This entirely absorbs the demand bottleneck, rendering the **2.000.000 €** investment in a redundant machine **OBSOLETE**.
- **Net CapEx Saved:** 1.950.000 €

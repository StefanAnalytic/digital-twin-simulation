import simpy
import numpy as np
import pandas as pd
from scipy import stats

class TwinTracker:
    def __init__(self):
        self.wip_log = []
        self.throughput_log = []
        
    def record_wip(self, wip_level):
        self.wip_log.append(wip_level)
        
    def get_truncation_point(self, window=50, variance_threshold=0.05):
        """
        Welch's Method (Moving Average Heuristic) zur Bestimmung des Steady-State.
        Schneidet den Initialization Bias ab.
        """
        if len(self.wip_log) < window * 2:
            return 0
            
        wip_series = pd.Series(self.wip_log)
        rolling_mean = wip_series.rolling(window=window).mean().dropna()
        
        # Finde den Punkt, an dem die Varianz des Moving Average stabil wird
        for i in range(len(rolling_mean) - window):
            window_var = np.var(rolling_mean.iloc[i:i+window])
            if window_var < variance_threshold:
                return i + window # Steady-State erreicht
        return len(self.wip_log) // 2 # Fallback

class TwinValidator:
    @staticmethod
    def validate_throughput(sim_throughput, hist_throughput):
        """
        Two-Sample Kolmogorov-Smirnov Test (KS-Test).
        Nullhypothese: Beide Verteilungen sind identisch.
        """
        stat, p_value = stats.ks_2samp(sim_throughput, hist_throughput)
        print(f"KS-Test -> p-value: {p_value:.4f}")
        
        # Guard bricht ab, wenn p < 0.05 (Verteilungen sind signifikant unterschiedlich)
        assert p_value >= 0.05, f"Validation Failed: p-value {p_value:.4f} < 0.05. Twin spiegelt Realität nicht wider!"
        print("✅ TwinValidator PASSED: Simulation gleicht der historischen Realität.")

class ManufacturingTwin:
    def __init__(self, env, tracker, buffer_capacity, weibull_shape, weibull_scale):
        self.env = env
        self.tracker = tracker
        self.machine = simpy.Resource(env, capacity=1)
        self.buffer = simpy.Container(env, capacity=buffer_capacity, init=0)
        self.parts_produced = 0
        
        # MTBF Parameter (Weibull)
        self.k = weibull_shape
        self.lmbda = weibull_scale
        
    def time_to_failure(self):
        # Generiert Ausfallzeiten basierend auf der gefitteten Weibull-Verteilung
        return stats.weibull_min.rvs(self.k, scale=self.lmbda)
        
    def run_machine(self):
        while True:
            # Hol dir ein Teil aus dem Puffer (blockiert, wenn Puffer leer)
            yield self.buffer.get(1)
            
            # Stochastische Processing Time (Normalverteilt, z.B. 5 min pro Teil)
            processing_time = max(1.0, np.random.normal(5.0, 0.5))
            
            # Maschinenausfall-Logik (vereinfacht für Durchsatz-Check)
            if np.random.rand() < (1.0 / self.time_to_failure()):
                # Maschine ist kaputt, Reparaturzeit (MTTR) anwenden
                repair_time = np.random.exponential(60.0) # z.B. 60 Min Reparatur
                yield self.env.timeout(repair_time)
                
            yield self.env.timeout(processing_time)
            self.parts_produced += 1
            self.tracker.record_wip(self.buffer.level)
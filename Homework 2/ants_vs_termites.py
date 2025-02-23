import numpy as np
import pandas as pd

class WAR:
    def __init__(self):
        self.prior = {'Ants': 0.7, 'Termites': 0.3}
        self.tactics = {'Ants': {'Chemical': 0.8, 'Physical': 0.6, 'Marking': 0.9}, 'Termites': {'Chemical': 0.4, 'Physical': 0.7, 'Marking': 0.5}}
    
    def calculate_probabilities(self):
        joint_probs = {}

        for s in self.prior.keys():
            p_s = self.prior[s]
            probs = self.tactics[s]

            for i in range(8):
                c = bool(i & 1)
                p = bool(i & 2)
                m = bool(i & 4)

                p_c = probs['Chemical'] if c else (1 - probs['Chemical'])
                p_p = probs['Physical'] if p else (1 - probs['Physical'])
                p_m = probs['Marking'] if m else (1 - probs['Marking'])

                joint_prob = p_s * p_c * p_p * p_m
                joint_probs[(s, c, p, m)] = joint_prob

        return pd.Series(joint_probs)
    
    def simulate_battle(self, N):
        initiators = np.random.choice(list(self.prior.keys()), size = N, p = list(self.prior.values()))

        chem_succ = np.zeros(N)
        phys_succ = np.zeros(N)
        mark_succ = np.zeros(N)
        
        for i in range(N):
            s = initiators[i]

            chem_succ[i] = np.random.random() < self.tactics[s]['Chemical']
            phys_succ[i] = np.random.random() < self.tactics[s]['Physical']
            mark_succ[i] = np.random.random() < self.tactics[s]['Marking']
        
        results = pd.DataFrame({'Initiator': initiators, 'Chemical': chem_succ, 'Physical': phys_succ, 'Marking': mark_succ})
        joint_counts = results.groupby(['Initiator', 'Chemical', 'Physical', 'Marking']).size()
        joint_probs = joint_counts / N
        
        return joint_probs

    def compare_probabilities(self, N):
        a = self.calculate_probabilities()
        s = self.simulate_battle(N)
    
        c = pd.DataFrame({'Analytic': a, 'Simulated': s}).fillna(0)
        c['Differance'] = abs(c['Analytic'] - c['Simulated'])

        return c

def run_analysis():
    sim = WAR()
    N_values = [1, 100, 1000, 10000, 100000, 1000000]

    print("Analysis")

    for N in N_values:
        comp = sim.compare_probabilities(N)
        max_diff = comp['Differance'].max()
        mean_diff = comp['Differance'].mean()
        print(f"\nN = {N:,}")
        print(f"Maximum differance: {max_diff:.6f}")
        print(f"Mean differance: {mean_diff:.6f}")
        
        if N == 100000:
            print("\ncomparison for N = 100,000:")
            print(comp.round(6).head())

if __name__ == "__main__":
    run_analysis()
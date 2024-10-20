import numpy as np
from hmmlearn import hmm
import matplotlib.pyplot as plt

# Ustawienie losowych wartości dla powtarzalności wyników
np.random.seed(42)

# Generowanie syntetycznych danych: zwroty
# 1000 prób
n_samples = 1000
# Przykładowe zwroty dla hossy (małe wartości dodatnie) i bessy (małe wartości ujemne)
returns_hossa = np.random.normal(loc=0.01, scale=0.02, size=n_samples // 2)  # Hossa
returns_bessa = np.random.normal(loc=-0.01, scale=0.02, size=n_samples // 2)  # Bessa
returns = np.concatenate([returns_hossa, returns_bessa])

# Reshape do formatu, który wymaga HMM
returns = returns.reshape(-1, 1)

# Definiowanie modelu HMM
model = hmm.GaussianHMM(n_components=2, covariance_type="full", n_iter=1000)

# Fitting modelu na danych
model.fit(returns)

# Przewidywanie stanu na podstawie danych zwrotów
hidden_states = model.predict(returns)

# Wizualizacja wyników
plt.figure(figsize=(15, 8))
plt.plot(returns, label='Zwroty')
plt.plot(hidden_states, label='Ukryte stany', alpha=0.7)
plt.title('Model HMM: Hossa i Bessa')
plt.xlabel('Czas')
plt.ylabel('Zwroty')
plt.legend()
plt.grid()
plt.show()

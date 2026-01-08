import numpy as np
import os
import time

def asteroid_impact_analysis():
    # --- KONFIGURACJA (Pobierana z Dockera) ---
    N_SIMULATIONS = int(os.getenv('SIMULATIONS', 100000))
    SIM_ID = os.getenv('SIM_ID', 'Material-Test')
    
    # Typ materiału: 1=Lód, 2=Kamień, 3=Żelazo
    MATERIAL_TYPE = int(os.getenv('MATERIAL_TYPE', 2))

    print(f"[{SIM_ID}] ROZPOCZYNAM ANALIZĘ INŻYNIERSKĄ...")
    print(f"[{SIM_ID}] Model: Wytrzymałość na ciśnienie dynamiczne (Ram Pressure)")
    
    # --- DANE MATERIAŁOWE ---
    if MATERIAL_TYPE == 1: 
        density = 1000.0       # kg/m3 (Lód)
        strength = 1.0 * 10**6 # Pa (Słabe)
        mat_name = "LÓD (Kometa)"
    elif MATERIAL_TYPE == 3: 
        density = 7800.0       # kg/m3 (Żelazo)
        strength = 200.0 * 10**6 # Pa (Bardzo mocne)
        mat_name = "ŻELAZO (Meteoryt)"
    else: 
        density = 2600.0       # kg/m3 (Kamień)
        strength = 10.0 * 10**6 # Pa (Średnie)
        mat_name = "KAMIEŃ (Asteroida)"

    print(f"[{SIM_ID}] Materiał: {mat_name} | Gęstość: {density} | Wytrzymałość: {strength/1e6} MPa")

    # --- SYMULACJA MONTE CARLO (Numpy) ---
    start_time = time.time()
    
    # 1. Losujemy Średnice (rozkład normalny: 50m +/- 10m)
    diameter = np.random.normal(50.0, 10.0, N_SIMULATIONS)
    diameter = np.maximum(diameter, 1.0) # Zabezpieczenie przed ujemną
    
    # 2. Losujemy Prędkości (18 km/s +/- 3 km/s) -> na m/s
    velocity = np.random.normal(18.0, 3.0, N_SIMULATIONS) * 1000.0 

    # --- OBLICZENIA FIZYCZNE ---
    # Ciśnienie dynamiczne działające na czoło asteroidy: P = rho_air * v^2
    # Przyjmujemy gęstość atmosfery w punkcie krytycznym ~1.0 kg/m3
    impact_pressure = 1.0 * velocity**2
    
    # Energia kinetyczna (dla statystyki) w Kilotonach TNT
    mass = (4/3) * np.pi * (diameter/2)**3 * density
    energy_kt = (0.5 * mass * velocity**2) / (4.184 * 10**12)

    # --- WARUNEK ZNISZCZENIA ---
    # Jeśli ciśnienie > wytrzymałość -> Asteroida wybucha w powietrzu (Airburst)
    # Jeśli ciśnienie < wytrzymałość -> Asteroida uderza w ziemię (Impact)
    fragmented = impact_pressure > strength
    
    ground_impacts = np.sum(~fragmented) # Ilość uderzeń w grunt
    airbursts = np.sum(fragmented)       # Ilość wybuchów w powietrzu
    
    duration = time.time() - start_time

    # --- RAPORT KOŃCOWY ---
    print(f"[{SIM_ID}] --- WYNIKI ---")
    print(f"[{SIM_ID}] Przetworzono przypadków: {N_SIMULATIONS} w czasie {duration:.2f}s")
    print(f"[{SIM_ID}] -> Wybuchy w atmosferze (bezpieczne): {airbursts}")
    print(f"[{SIM_ID}] -> Uderzenia w Ziemię (KRATER): {ground_impacts}")
    print(f"[{SIM_ID}] -> Średnia energia uderzenia: {np.mean(energy_kt):.2f} kT TNT")
    
    risk_level = (ground_impacts / N_SIMULATIONS) * 100
    print(f"[{SIM_ID}] RYZYKO UDERZENIA W GRUNT: {risk_level:.2f}%")

if __name__ == "__main__":
    asteroid_impact_analysis()
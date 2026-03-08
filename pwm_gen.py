import os

# Mülakat Parçalayan PWM Jeneratörü v2.0
# Frekans ve Duty Cycle bazlı gerçek zamanlı hesaplama
frekans = 50000        # 100 kHz (Periyot = 10 mikrosaniye)
duty_cycle = 0.50       # %50 Doluluk (5us açık, 5us kapalı)
v_on = 3.3             # MOSFET Gate tokatlama voltajı
v_off = 0.0             # Kapalı voltajı
t_gecis = 20e-9         # 20ns Yükselme/Düşme süresi (Rise/Fall)
simulasyon_suresi = 0.1    # LTspice'taki .tran 5m ile tam uyumlu olması için 5ms

periyot = 1.0 / frekans
t_on = periyot * duty_cycle

# Dosya yolu belirleme (Dosyanın yanına üretir)
bulunulan_klasor = os.path.dirname(os.path.abspath(__file__))
dosya_yolu = os.path.join(bulunulan_klasor, "pwm_sinyali.txt")

with open(dosya_yolu, "w") as f:
    t = 0.0
    while t < simulasyon_suresi:
        # Başlangıç (0V)
        f.write(f"{t:.12f}\t{v_off:.1f}\n")
        
        # MOSFET Açılıyor (Rising Edge)
        t += t_gecis
        f.write(f"{t:.12f}\t{v_on:.1f}\n")
        
        # MOSFET Açık Kalıyor (ON Time)
        t += (t_on - t_gecis)
        f.write(f"{t:.12f}\t{v_on:.1f}\n")
        
        # MOSFET Kapanıyor (Falling Edge)
        t += t_gecis
        f.write(f"{t:.12f}\t{v_off:.1f}\n")
        
        # MOSFET Kapalı Kalıyor (OFF Time - Periyodun kalanı)
        t += (periyot - t_on - t_gecis)
        # Periyot sonu noktasını yazıyoruz
        f.write(f"{t:.12f}\t{v_off:.1f}\n")

print(f"BOMBA GİBİ HAZIR! Dosya konumu:\n{dosya_yolu}")
print(f"Hesaplanan T_on: {t_on*1e6:.2f} us | Periyot: {periyot*1e6:.2f} us")
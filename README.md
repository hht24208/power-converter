# STM32 Kontrollü SEPIC Güç Dönüştürücü (Power Converter)

Bu proje, geniş giriş voltajı aralıklarında çalışabilen, yazılım tabanlı (STM32) PID kontrolüne sahip bir SEPIC güç dönüştürücüsünün donanım mimarisini ve LTspice üzerindeki matematiksel modellemelerini içermektedir.

## 1. Güç Katı ve Donanım Mimarisi
Aşağıdaki şema, SEPIC topolojisinin güç katını ve geri besleme (feedback) mekanizmasını göstermektedir. Sistemde yüksek hızlı MOSFET anahtarlaması için **TC4427** gate sürücü kullanılmış olup, akım ve gerilim okumaları **LM358** op-ampları üzerinden mikrodenetleyicinin ADC pinlerine uygun hale getirilmiştir.

![SEPIC Devre Şeması](images/devre.png)

## 2. Matematiksel Modelleme ve PID Kontrolcü
Sistemin 4. dereceden non-lineer yapısı (sağ yarı düzlem sıfırı ve rezonans frekansları), rastgele PID katsayılarıyla kontrol edilemez. Bu nedenle LTspice üzerinde sistemin transfer fonksiyonuna uygun bir **Type-II/III Kompansatör** tasarlanmış ve Laplace dönüşümleriyle s-domain (karmaşık frekans düzlemi) üzerinde modellenmiştir.

![PID Kontrolcü ve Laplace Denklemi](images/controller.png)

## 3. Geçici Hal Yanıtı (Transient Response) ve Inrush Yönetimi
Aşağıdaki osiloskop çıktısı, sisteme aniden 12V (Step Input) uygulandığında donanımın ve kontrolcünün verdiği fiziksel tepkiyi göstermektedir. 
* İlk milisaniyelerde SEPIC topolojisinin doğası gereği uçan kondansatör üzerinden geçen **Inrush Current (Başlangıç Şoku)** voltajı anlık olarak yükseltir.
* Kontrolcü bu durumu anında tespit edip PWM görev döngüsünü (Duty Cycle) %0'a çeker.
* Sistem 11. milisaniyede hedef voltaj olan **5V** seviyesine kusursuz ve stabil bir şekilde (sıfır kalıcı hal hatası ile) oturur.

![Osiloskop Çıktısı - 12V Inrush ve 5V Regülasyonu](images/osiloskop.png)

---
*Not: Bu simülasyonlar, gerçek dünyadaki PCB parazitikleri ve komponent toleransları göz önünde bulundurularak, STM32 üzerinde yazılacak C tabanlı dijital kontrol algoritmasına (Digital Power Supply) temel oluşturmak için tasarlanmıştır.*
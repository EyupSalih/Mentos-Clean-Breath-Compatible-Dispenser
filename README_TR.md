# Mentos Clean Breath V7 FUNCTIONAL CAD

Bu sürüm V6 mimarisinin devamı değildir. **V5’in anlaşılır 15+15 şarjör + yay + follower + lineer shuttle mantığına geri dönülmüş**, kullanıcı geri bildirimleri hedefli olarak uygulanmıştır.

## Temel mimari
- 30 tablet kapasite: 2 adet çıkarılabilir 15’li şarjör.
- V5 tipi metal ana yay + follower sistemi korunmuştur.
- Follower tek parça üzerinde **ön ve arka iki karşılıklı sapa** sahiptir ve şarjör içindeki iki simetrik J/bayonet cebinde kilitlenir.
- Ana gövdenin dış yüzünde uzun follower kanalı **yoktur**; dış kabuk kapalıdır.
- Gövdenin yalnız sol yanında küçük gömme bir release butonu görünür; içerideki ortak release bar iki follower kilidini aynı anda açar.
- Şarjörler yaylar hâlâ kilitliyken gövdeye takılır; **alt kapak kapandıktan sonra** yan butonla yaylar aktive edilir.
- Alt kapak rutin vidasızdır; tam tabanı örten, labirent bindirmeli sürgülü dış kapaktır ve ball-plunger detent ile tutulur.
- Üst kapakta dört gerçek M2.5 vida yolu bulunur: top-cap ve transfer deck geçişli, alt gövdede heat-set insert bossları vardır.
- Üst shuttle iki katmanlıdır: taşıyıcı cep + **cutoff tabakası**. Shuttle bir tarafa çekildiğinde geride ikinci tabletin çıkacağı açık boşluk bırakmak yerine feed deliklerini katı yüzeyle kapatır.
- Thumb tab top-cap’in yaklaşık **3.3 mm üzerinde** kalır; parmakla erişim V5’e göre büyütülmüştür.
- Çıkışta TPU toz/dökülme flap’i bulunur.

## Doldurma ve devreye alma sırası
1. Şarjör cihaz dışında tutulur; TPU feed ring çıkarılır.
2. Refill push-twist tool ile follower aşağı bastırılır ve yaklaşık 18° döndürülerek iki sap birden çift J kilide alınır.
3. 15 tablet doldurulur, TPU feed ring yeniden takılır.
4. Aynı işlem ikinci şarjör için yapılır.
5. İki şarjör de **ana yayları kilitli** halde gövdeye alttan sürülür.
6. Tam tabanı kapatan alt sürgülü dış kapak kapatılır.
7. Bundan sonra yandaki tek recessed release butonuna basılır; iç release bar her iki follower kilidini aynı anda çözer ve yaylar tabletleri yukarı besler.

## Şeker alma mantığı
- Shuttle merkezde güçlü detent ile tutulur.
- Bir tarafa kaydırıldığında ilgili taşıyıcı cep merkez çıkışa gelir.
- Shuttle’ın alt cutoff katmanı, shuttle kaynak konumdan ayrılırken **her iki feed deliğini de kapatır**; ikinci tablet boş lateral hacme yükselemez.
- Tablet merkezdeki gerçek çıkış yolundan TPU flap üzerinden çekilir.
- Shuttle merkeze döndüğünde boş cep tekrar ilgili feed penceresiyle hizalanır.

## FreeCAD’de önce açılacak dosyalar
- `ASSEMBLY_STATES/01_COMPLETE_30_LOADED_RELEASED.step`
- `ASSEMBLY_STATES/02_CUTAWAY_INTERNALS.step`
- `ASSEMBLY_STATES/03_MAGAZINE_DOUBLE_J_REFILL_SEQUENCE.step`
- `ASSEMBLY_STATES/04_CLOSE_CASE_THEN_SIDE_BUTTON_DUAL_RELEASE.step`
- `ASSEMBLY_STATES/05_SHUTTLE_CUTOFF_ANTI_JAM_STATES.step`
- `ASSEMBLY_STATES/06_FULL_SLIDING_BOTTOM_COVER_SERVICE.step`
- `ASSEMBLY_STATES/07_TOP_REAL_SCREW_INSTALLATION.step`
- `ASSEMBLY_STATES/08_OUTPUT_EXTRACTION_SEQUENCE.step`
- `ASSEMBLY_STATES/09_EXPLODED_ALL_PARTS.step`

## CAD audit sonucu
- Status: **CAD_GATE_PASS**
- Kritik CAD gate hatası: **0**
- Thumb-tab yükseklik kontrolü: **3.3 mm top-cap üstü**
- Alt dış kapak kapsama ölçüsü: **59.0 mm genişlik, 30.7 mm derinlik**
- Release bar 0–2.45 mm sweep: gövde/şarjör rijit çakışması **0**
- Tam basmada iki locked follower ile fonksiyonel temas: **PASS**
- Maksimum tablet zarfı: Ø11.55 × 6.20 mm çıkış/sweep kontrolü **PASS**
- Dispense stoplarında iki source feed’in cutoff ile fiziksel blokajı: **PASS**

## Önemli sınır
CAD gate fiziksel kullanım sertifikası değildir. Baskı sonrası gerçek Mentos parti toleransı, yay kuvvet eğrisi, TPU sertliği/gıda uygunluğu, yazıcıya özgü sürgü toleransı ve toz sızdırmazlığı mutlaka doğrulanmalıdır.

## Sonradan entegre edilen V7 parça revizyonları
Bu paket aşağıdaki son kullanıcı onaylı geometrileri ana projeye entegre eder:
- `01_lower_chassis_closed_shell`: şarjörleri daha iyi merkezleyen/tutan MAGAZINE_RETAINED kasa revizyonu.
- `03_top_cap_real_screw_access`: ön gereksiz açıklığı gövdeyle bütünleşik kapatılmış ve 11 numaralı kapak için pim menteşe noktaları eklenmiş revizyon.
- `08_dual_pocket_CUTOFF_shuttle`: üstteki şeker ceplerini dış ortamdan kapatan düz kapalı shuttle revizyonu.
- `11_TPU_output_dust_flap`: 03 üzerindeki pimlerle çalışan delikli/pimli gerçek menteşe revizyonu.

`ASSEMBLY_STATES` klasöründeki STEP dosyaları da bu dört güncel parçayla yeniden oluşturulmuştur.


## Son entegre revizyon (02 + 03)
Bu ZIP içindeki 02 ve 03 STEP/STL dosyaları son revizyondur. 9 adet ASSEMBLY_STATES STEP dosyası da aynı güncel geometrilerle yeniden oluşturulmuştur. Ayrıntı: `AUDIT/V7_LATEST_02_03_INTEGRATION_NOTE_TR.md`.

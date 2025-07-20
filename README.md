# n8n ile Yapay Zeka Destekli Fishbone Analizi Projesi

Bu proje, bir chat ekranından veya herhangi bir HTTP istemcisinden gelen bir "sorun" metnini, n8n üzerinde çalışan bir yapay zeka modeli ile analiz ederek, sonuç olarak yapılandırılmış bir Fishbone (Balık Kılçığı) diyagramı, kilit sorular ve çözüm önerileri üreten bir iş akışı içerir.

## Projenin Amacı

Kullanıcıların belirttiği problemlere yönelik, kalite yönetimi standartlarına uygun, derinlemesine ve metodik bir kök neden analizi sunan otomatik bir sistem oluşturmaktır. Tüm mantık, harici bir sunucuya ihtiyaç duymadan, tamamen n8n içinde çalışır.

## Dahil Olan Dosyalar

-   `README.md`: Bu dosya. Projeye genel bir bakış sunar.
-   `TODO.md`: Proje geliştirme sürecindeki görev listesi.
-   `ai_prompt.txt`: Yapay zeka modeline, analizini nasıl yapması gerektiğini adım adım anlatan detaylı komut istemi (prompt).
-   `n8n_fishbone_ai_workflow.json`: n8n'e doğrudan aktarılabilen, projenin tüm mantığını içeren iş akışı tanımı.

## Kurulum ve Kullanım

Bu sistemi çalıştırmak için aşağıdaki adımları izleyin:

### Adım 1: n8n İş Akışını İçe Aktarma

1.  n8n arayüzünüzü açın.
2.  Yeni bir iş akışı (workflow) oluşturun veya mevcut bir tanesine geçin.
3.  Ekranın herhangi bir yerine sağ tıklayın ve "Import from File" (Dosyadan İçe Aktar) seçeneğini seçin.
4.  Bu projedeki `n8n_fishbone_ai_workflow.json` dosyasını seçin. İş akışı tuvalinize yüklenecektir.

### Adım 2: Yapay Zeka Kimlik Bilgilerini Ayarlama

1.  Yüklenen iş akışındaki "AI Analysis" (Yapay Zeka Analizi) adlı düğüme tıklayın.
2.  Sol taraftaki panelde, "Credentials" (Kimlik Bilgileri) bölümünü göreceksiniz.
3.  Burada, kendi OpenAI (veya uyumlu başka bir LLM sağlayıcısı) API anahtarınızı içeren kimlik bilgisini seçin veya oluşturun. Bu adım, iş akışının yapay zeka servisine bağlanabilmesi için zorunludur.
4.  İş akışını sağ üst köşedeki **"Activate"** düğmesine basarak aktif hale getirin.

### Adım 3: İş Akışını Test Etme

İş akışı artık dışarıdan gelecek istekleri dinlemeye hazırdır. Aşağıdaki `curl` komutunu bir terminalde çalıştırarak sistemi test edebilirsiniz.

**Not:** `YOUR_N8N_WEBHOOK_URL` kısmını, n8n'deki "Webhook" düğümüne tıkladığınızda görünen kendi "Test URL" veya "Production URL" adresinizle değiştirmeyi unutmayın.

```bash
curl -X POST YOUR_N8N_WEBHOOK_URL \
-H "Content-Type: application/json" \
-d '{
  "sorun": "Müşteri destek ekibinin yanıt süreleri son çeyrekte %50 arttı."
}'
```

### Beklenen Çıktı

`curl` komutuna yanıt olarak, yapay zekanın `ai_prompt.txt` dosyasındaki talimatlara göre ürettiği, aşağıdaki yapıya benzer bir JSON nesnesi alacaksınız:

```json
{
  "problem_statement": "Müşteri destek ekibinin yanıt sürelerinin son çeyrekte %50 artması.",
  "fishbone_analysis": {
    "Manpower": [
      {
        "cause": "Yetersiz personel sayısı",
        "sub_causes": ["Artan talep karşısında işe alım yapılmaması", "Mevcut personelin iş yükünün fazla olması"]
      },
      {
        "cause": "Eğitim eksikliği",
        "sub_causes": ["Yeni ürünler hakkında yetersiz bilgi", "Etkili zaman yönetimi eğitimi verilmemesi"]
      }
    ],
    "Methods": [
      {
        "cause": "Verimsiz ticket yönetim süreci",
        "sub_causes": ["Ticket'ların önceliklendirilmemesi", "Standart yanıt şablonlarının kullanılmaması"]
      }
    ],
    "Machinery": [
      {
        "cause": "Yavaş çalışan CRM sistemi",
        "sub_causes": ["Sistemin eski olması", "Gereksiz eklentiler"]
      }
    ],
    "Materials": [],
    "Measurement": [],
    "Mother Nature": [],
    "Money": []
  },
  "key_questions": [
    "Son çeyrekteki talep artışının tam oranı nedir?",
    "Personel başına düşen günlük ortalama ticket sayısı nedir?",
    "Mevcut CRM sisteminin performansını yavaşlatan belirli bir modül var mı?"
  ],
  "solution_proposals": [
    "Acil olarak 2 yeni müşteri destek uzmanı işe alınması.",
    "Tüm ekibe yönelik zaman yönetimi ve yeni ürünler hakkında eğitim düzenlenmesi.",
    "CRM sisteminin performansını artırmak için bir teknik analiz yapılması ve gerekiyorsa güncellenmesi."
  ]
}
```

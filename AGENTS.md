# Fishbone - n8n Entegrasyonu Teknik Gereksinimleri

Bu doküman, Fishbone ve n8n sistemleri arasında MCP (Master Control Program) katmanı kullanılarak yapılacak entegrasyonun teknik gereksinimlerini ve kısıtlarını tanımlar.

## 1. Sistem Bileşenleri
- **Fishbone Sistemi:** Kök neden analizi verilerinin kaynağı.
- **MCP (Master Control Program):** Entegrasyon ara katmanı. API uç noktalarını barındırır, kimlik doğrulama ve temel veri doğrulama işlemlerini yapar.
- **n8n:** İş akışı otomasyon platformu. MCP'den gelen verileri işler.

## 2. Veri Akışı ve Yapısı

### Fishbone'dan MCP'ye Gönderilecek Veri Yapısı (JSON)
MCP, aşağıdaki JSON yapısını kabul edecek şekilde bir API uç noktası sağlamalıdır:
```json
{
  "diagram_id": "string",
  "problem_statement": "string",
  "categories": [
    {
      "category_name": "string",
      "causes": [
        {
          "cause_text": "string",
          "sub_causes": [
            {
              "cause_text": "string",
              "sub_causes": []
            }
          ]
        }
      ]
    }
  ]
}
```

### MCP'den n8n'e Veri Aktarımı
MCP, yukarıdaki JSON verisini değiştirmeden n8n'deki bir Webhook'a POST isteği ile iletecektir.

## 3. API Uç Noktası (Endpoint)

- **MCP Endpoint:** `/api/fishbone`
- **Metot:** `POST`
- **Başlıklar (Headers):**
  - `Content-Type: application/json`
  - `Authorization: Bearer <SIMPLE_SECURE_TOKEN_123>`

## 4. Kimlik Doğrulama (Authentication)

- **Fishbone -> MCP:** `Authorization` başlığında gönderilecek bir Bearer Token (`SIMPLE_SECURE_TOKEN_123`) ile kimlik doğrulama yapılacaktır. Token, MCP tarafında doğrulanacaktır.
- **MCP -> n8n:** n8n Webhook URL'si, tahmin edilmesi zor, kriptografik olarak güvenli bir karakter dizisi içerecektir. Bu, temel bir güvenlik katmanı sağlar.

## 5. Hata Yönetimi (Error Handling)

- **MCP Hata Kodları:**
  - `400 Bad Request`: Gelen JSON verisi eksik veya hatalı ise.
  - `401 Unauthorized`: `Authorization` başlığı eksik veya geçersiz ise.
  - `500 Internal Server Error`: MCP'de veya n8n'e veri gönderimi sırasında beklenmedik bir hata oluşursa.
- **Loglama:** Tüm başarılı ve hatalı istekler, MCP'de zaman damgası, kaynak IP ve istek gövdesi (body) özeti ile loglanacaktır.
- **n8n Hata Yönetimi:** n8n iş akışındaki hatalar, n8n'in dahili "Error Workflow" mekanizması ile yönetilecektir.

## 6. Beklenen Sonuç
Bu entegrasyon sonucunda, bir Fishbone diyagramı oluşturulduğunda veya güncellendiğinde, verileri güvenli bir şekilde MCP üzerinden n8n'e akacak ve burada otomatik iş akışlarını tetikleyecektir.

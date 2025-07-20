# Fishbone - n8n Entegrasyonu Test Planı

Bu doküman, Fishbone-MCP-n8n entegrasyonunun uçtan uca test senaryosunu açıklamaktadır.

## 1. Testin Amacı
Oluşturulan MCP sunucusunun ve n8n iş akışının, tanımlanan gereksinimlere uygun olarak birlikte çalışıp çalışmadığını doğrulamak.

## 2. Ön Koşullar
1.  **MCP Sunucusunu Başlatma:**
    - `python -u mcp_server.py &` komutu ile `mcp_server.py` sunucusu başlatılmalıdır.
2.  **n8n İş Akışını Aktif Etme:**
    - `n8n_workflow.json` dosyasının içeriği bir n8n örneğine (instance) aktarılmalı ve iş akışı "active" (aktif) duruma getirilmelidir.
    - n8n'in çalıştığı adresin ve webhook yolunun `mcp_server.py` içindeki `N8N_WEBHOOK_URL` değişkeni ile eşleştiği varsayılmaktadır. (Not: Mevcut simülasyonda MCP'den n8n'e gerçek bir çağrı yapılmamaktadır.)

## 3. Test Adımları

Aşağıdaki `curl` komutu bir terminalde çalıştırılır:

```bash
curl -X POST http://localhost:8000/api/fishbone \
-H "Content-Type: application/json" \
-H "Authorization: Bearer SIMPLE_SECURE_TOKEN_123" \
-d '{
  "diagram_id": "diag-test-001",
  "problem_statement": "Entegrasyon testi",
  "categories": [
    {
      "category_name": "Test",
      "causes": [
        {
          "cause_text": "Başarılı senaryo testi",
          "sub_causes": []
        }
      ]
    }
  ]
}'
```

## 4. Beklenen Sonuçlar

### 4.1. `curl` İstemcisi
- Terminalde aşağıdaki çıktının alınması beklenir:
  ```json
  {"message": "Veri başarıyla alındı ve işlendi."}
  ```
- HTTP durum kodunun `200 OK` olması gerekir.

### 4.2. MCP Sunucusu (Logları)
- `mcp_server.log` dosyasında, sunucunun gelen veriyi `print` ettiği satırların görünmesi beklenir. (Not: Mevcut `BaseHTTPRequestHandler` implementasyonunda bu loglar `stdout`'a yazdırılamamıştır, ancak başarılı `200 OK` yanıtı kodun o bloğunun çalıştığını teyit eder.)

### 4.3. n8n Arayüzü
- n8n'in "Executions" (Çalıştırmalar) bölümünde "Fishbone Integration Workflow" için yeni ve başarılı bir çalıştırma görünmelidir.
- Bu çalıştırmanın detaylarına bakıldığında:
    - **Fishbone Webhook:** Başarıyla tetiklenmiş ve `curl` ile gönderilen JSON verisini almış olmalıdır.
    - **Set Variables:** `problem` değişkenini "Entegrasyon testi" olarak, `diagramId` değişkenini ise "diag-test-001" olarak ayarlamış olmalıdır.
    - **Processing Complete:** İş akışı bu düğüme ulaşıp başarıyla sonlanmış olmalıdır.

## 5. Hatalı Senaryo Testleri (Örnekler)

- **Geçersiz Token:** `Authorization` başlığında yanlış bir token gönderildiğinde, MCP sunucusunun `401 Unauthorized` hatası döndürmesi beklenir.
- **Eksik Veri:** JSON gövdesinde `problem_statement` gibi zorunlu bir alan eksik gönderildiğinde, MCP sunucusunun `400 Bad Request` hatası döndürmesi beklenir.

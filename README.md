# Fishbone - n8n Entegrasyonu Projesi

Bu proje, bir Fishbone (Balık Kılçığı Diyagramı) sisteminden gelen verileri, bir n8n iş akışı otomasyon platformuna entegre etmeyi amaçlamaktadır. Entegrasyon, ara katman olarak görev yapan bir MCP (Master Control Program) üzerinden gerçekleştirilir.

## Projenin Amacı

Kök neden analizi için kullanılan Fishbone diyagramı verilerinin, otomatik iş akışları (raporlama, görev oluşturma, bildirim gönderme vb.) tetiklemek üzere n8n'e güvenli ve yapılandırılmış bir şekilde aktarılmasını sağlamak.

## Sistem Mimarisi

Entegrasyon 3 ana bileşenden oluşur:

1.  **Fishbone Sistemi (Kaynak):** Analiz verilerini oluşturur ve MCP'ye gönderir.
2.  **MCP - Master Control Program (Ara Katman):** Bu repodaki `mcp_server.py` ile simüle edilmiştir. Gelen veriler için bir API uç noktası sağlar, kimlik doğrulaması yapar ve veriyi n8n'e iletir.
3.  **n8n (Hedef):** MCP'den gelen veriyi alır ve `n8n_workflow.json` içinde tanımlanan iş akışını çalıştırır.

Veri akışı: `Fishbone -> MCP -> n8n`

## Dosya Yapısı

-   `README.md`: Bu dosya. Projeye genel bakış sağlar.
-   `AGENTS.md`: Projenin detaylı teknik gereksinimlerini, veri yapılarını, API endpoint'lerini ve kimlik doğrulama yöntemlerini tanımlar.
-   `mcp_server.py`: MCP sunucusunu simüle eden bir Python betiği. Gelen `POST` isteklerini dinler, token doğrulaması yapar ve veriyi işler.
-   `n8n_workflow.json`: MCP'den gelen verileri almak ve işlemek için tasarlanmış n8n iş akışının JSON formatındaki tanımı. Bu dosya, n8n'e doğrudan içe aktarılabilir.
-   `TESTING.md`: Entegrasyonun uçtan uca nasıl test edileceğini açıklayan test planı ve senaryoları.

## Kurulum ve Çalıştırma

1.  **MCP Sunucusunu Başlatma:**
    ```bash
    python mcp_server.py
    ```
    Sunucu, `localhost:8000` adresinde çalışmaya başlayacaktır.

2.  **n8n İş Akışını Kurma:**
    - Bir n8n örneğinde (instance), yeni bir iş akışı oluşturun.
    - "Import from File" (Dosyadan İçe Aktar) seçeneğini kullanarak `n8n_workflow.json` dosyasını yükleyin.
    - İş akışını kaydedin ve aktif hale getirin.

3.  **Entegrasyonu Test Etme:**
    - `TESTING.md` dosyasında belirtilen `curl` komutunu kullanarak MCP sunucusuna bir test isteği gönderin.
    - Testin başarılı olduğunu `curl` çıktısını ve n8n arayüzündeki çalıştırmaları (executions) kontrol ederek doğrulayın.

## Güvenlik Notu
`mcp_server.py` ve `AGENTS.md` dosyalarında kullanılan `SIMPLE_SECURE_TOKEN_123` token'ı sadece bir örnektir. Gerçek bir üretim ortamında, bu token daha karmaşık, rastgele oluşturulmuş ve güvenli bir şekilde (örneğin, ortam değişkenleri veya bir sır yönetim sistemi aracılığıyla) saklanmalıdır.

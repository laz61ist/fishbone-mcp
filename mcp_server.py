import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# AGENTS.md'den alınan sabitler
EXPECTED_TOKEN = "SIMPLE_SECURE_TOKEN_123"  # Gerçek uygulamada bu, güvenli bir yerden okunmalıdır.
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/fishbone-integration" # n8n webhook adresi

class MCPRequestHandler(BaseHTTPRequestHandler):
    """
    Gelen HTTP isteklerini işleyen request handler.
    """

    def _send_response(self, status_code, message):
        """Yardımcı fonksiyon: İstemciye yanıt gönderir."""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": message}).encode('utf-8'))

    def do_POST(self):
        """POST isteklerini işler."""
        if self.path == '/api/fishbone':
            # 1. Kimlik Doğrulama
            auth_header = self.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                self._send_response(401, "Authorization header eksik veya geçersiz.")
                return

            token = auth_header.split(' ')[1]

            if token != EXPECTED_TOKEN:
                self._send_response(401, "Geçersiz token.")
                return

            # 2. İstek Gövdesini Oku ve Ayrıştır
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
            except (json.JSONDecodeError, TypeError, KeyError):
                self._send_response(400, "Geçersiz JSON formatı veya Content-Length başlığı eksik.")
                return

            # 3. Veri Yapısını Doğrula (Temel düzeyde)
            required_keys = ["diagram_id", "problem_statement", "categories"]
            if not all(key in data for key in required_keys):
                self._send_response(400, f"Eksik anahtarlar. Gerekli anahtarlar: {required_keys}")
                return

            print("Gelen geçerli veri:")
            print(json.dumps(data, indent=2))

            # Normalde burada veri n8n'e gönderilir.
            # Bu simülasyonda sadece başarılı yanıt döndürüyoruz.
            # print(f"Veri n8n'e gönderiliyor: {N8N_WEBHOOK_URL}")

            self._send_response(200, "Veri başarıyla alındı ve işlendi.")

        else:
            self._send_response(404, "Endpoint bulunamadı.")

def run_server(server_class=HTTPServer, handler_class=MCPRequestHandler, port=8000):
    """Basit bir HTTP sunucusu başlatır."""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"MCP sunucusu {port} portunda başlatılıyor...")
    print(f"Kullanılacak Token: {EXPECTED_TOKEN}")
    print("Test etmek için aşağıdaki gibi bir cURL isteği kullanabilirsiniz:")
    print(f"""
curl -X POST http://localhost:{port}/api/fishbone \\
-H "Content-Type: application/json" \\
-H "Authorization: Bearer {EXPECTED_TOKEN}" \\
-d '{{
  "diagram_id": "diag-123",
  "problem_statement": "Ürün teslimatlarında gecikme",
  "categories": [
    {{
      "category_name": "İnsan",
      "causes": [
        {{ "cause_text": "Yetersiz personel" }},
        {{ "cause_text": "Eğitim eksikliği" }}
      ]
    }}
  ]
}}'
    """)
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()

#include <WiFi.h>

const char* AP_SSID = "千早爱音的超级ESP32";
const char* AP_PASS = "12345678";

WiFiServer server(8888);
WiFiClient client;
bool hasClient = false;
uint8_t buf[256];
int idx = 0;

void setup() {
    Serial.begin(115200);
    Serial2.begin(115200, SERIAL_8N1, 16, 17);
    
    WiFi.softAP(AP_SSID, AP_PASS);
    
    // 等待 AP IP 就绪，最多 3 秒
    unsigned long t = millis();
    while (WiFi.softAPIP() == IPAddress(0,0,0,0) && millis() - t < 3000) {
        delay(100);
    }
    Serial.println("AP IP: " + WiFi.softAPIP().toString());
    
    server.begin();
    Serial.println("Server started on port 8888");  // 确认 server 启动
}


void loop() {
    if (!hasClient) {
        client = server.available();
        if (client) hasClient = true;
    }

    // 批量读取
    while (Serial2.available() && idx < 256) {
        buf[idx++] = Serial2.read();
    }

    // 批量发送
    if (idx > 0 && hasClient) {
        client.write(buf, idx);
        idx = 0;
    }
}


// void loop() {
//     if (!hasClient) {
//         WiFiClient newClient = server.available();
//         if (newClient) {
//             client = newClient;
//             client.setNoDelay(true);   // 禁用 Nagle，立刻发送
//             hasClient = true;
//             Serial.println("Client connected!");
//         }
//     }

//     if (hasClient) {
//         if (!client.connected()) {
//             client.stop();
//             hasClient = false;
//             Serial.println("Client lost");
//         } else {
//             int count = 0;
//             while (Serial2.available()) {
//                 client.write((uint8_t)Serial2.read());
//                 count++;
//             }
//             if (count > 0) {
//                 client.flush();   // 确保数据立刻发出去
//             }
//         }
//     }

//     delay(1);
// }



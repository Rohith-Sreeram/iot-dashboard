# ESP32 Communication Guide

To connect your ESP32 to this cloud dashboard, use the following logic in your Arduino IDE sketch.

### Dependencies
- `WiFi.h`
- `HTTPClient.h`
- `ArduinoJson.h`

### Sample Code Snippet

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverUrl = "http://YOUR_COMPUTER_IP:5001/api/iot";

int entered = 10;
int left = 4;
int present = 6;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Create JSON payload
    StaticJsonDocument<200> doc;
    doc["entered"] = entered;
    doc["left"] = left;
    doc["present"] = present;
    
    String requestBody;
    serializeJson(doc, requestBody);

    int httpResponseCode = http.POST(requestBody);

    if (httpResponseCode > 0) {
      String response = http.getString();
      StaticJsonDocument<500> resDoc;
      deserializeJson(resDoc, response);

      // Check if server sent refresh values
      if (resDoc.containsKey("refresh")) {
        entered = resDoc["refresh"]["entered"];
        left = resDoc["refresh"]["left"];
        present = resDoc["refresh"]["present"];
        Serial.println("Updated values from Cloud Dashboard!");
      }
    }
    http.end();
  }
  delay(10000); // Sync every 10 seconds
}
```

### How to Run the System
1. **Install requirements**: `pip install -r requirements.txt`
2. **Start API Bridge**: `python api_bridge.py` (Keep this terminal open)
3. **Start Dashboard**: `streamlit run streamlit_app.py`
4. **Setup ESP32**: Flash the code above with your computer's local IP address.

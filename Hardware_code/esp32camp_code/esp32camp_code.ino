#include "esp_camera.h"
#include <WiFi.h>
#include <WebServer.h>

// Select camera model
#define CAMERA_MODEL_AI_THINKER
#include "camera_pins.h"

const char* ssid = "Ankit"; // WiFi Name SSID
const char* password = "88888862"; // WiFi Password

WebServer server(80);

void startCameraServer();

void handleStream() {
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    server.send(500, "text/plain", "Camera capture failed");
    return;
  }

  server.setContentLength(fb->len);
  server.sendHeader("Content-Type", "image/jpeg");
  server.send(200);

  for (size_t i = 0; i < fb->len; i++) {
    server.sendContent_P((char*)&fb->buf[i], 1);
  }

  esp_camera_fb_return(fb);
}

void setup() {
  Serial.begin(115200);
  Serial.println();

  camera_config_t config;
  // Camera configuration

  // Camera initialization
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  // WiFi connection
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  startCameraServer();

  Serial.print("Camera Ready! Use 'http://");
  Serial.print(WiFi.localIP());
  Serial.println("/stream' to connect");
}

void startCameraServer() {
  server.on("/stream", HTTP_GET, handleStream);
  server.begin();
}

void loop() {
  server.handleClient();
}

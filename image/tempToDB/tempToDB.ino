#include <WiFi.h> 
#include <DHT11.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char *ssid = "Anna333";
const char *password = "annaWiFi"; 

const char *serverAddress = "http://192.168.129.57:5000/post_data";
DHT11 dht11(15);

void setup() {
  Serial.begin(115200); //鮑率設定 115200
  WiFi.begin(ssid, password);//網路設定
  //等待網路連線
  while (WiFi.status() != WL_CONNECTED) {
  delay(1000);
  Serial.println("Connecting to WiFi...");
  }
  //連上網路並顯示目前 IP
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());
} 


void loop() {
  int temperature = 0;
  int humidity = 0; 
  int result = dht11.readTemperatureHumidity(temperature, humidity); 
  if (result == 0) {
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print(" °C\tHumidity: ");
    Serial.print(humidity);
    Serial.println(" %");
  } else {
  // Print error message based on the error code.
    Serial.println(DHT11::getErrorString(result));
  }

 // Create an object JSON
  JsonDocument jsonDoc;
  jsonDoc["temperature"] = temperature;
  jsonDoc["humidity"] = humidity;
   // Serializa el JSON en una cadena
  String payload;
  serializeJson(jsonDoc, payload);

   // Crea una instancia de HTTPClient
  HTTPClient http;
  Serial.println("Server Address: " + String(serverAddress));

  // Envía la solicitud POST al servidor
  http.begin(serverAddress); 

  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(payload);

  if (httpResponseCode > 0) {
    Serial.printf("HTTP Response code: %d\n", httpResponseCode);
    String response = http.getString();
    Serial.println(response);
  } else {
    Serial.printf("HTTP Request failed: %s\n",
    http.errorToString(httpResponseCode).c_str());
  } 
  http.end();
  delay(5000);
  Serial.println(); 
}

#include <SPI.h>
#include <Arduino.h>
#include <SPI.h>
#include <MFRC522.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define LED D1
#define RST_PIN D0 
#define SS_PIN D8
MFRC522 mfrc522(SS_PIN, RST_PIN); 
MFRC522::MIFARE_Key key;
MFRC522::StatusCode status;

 
const char *WIFI_SSID = "SSID"; 
const char *WIFI_PASSWORD = "PASSWORD"; 
const char *URL = "http://HOST:PORT"; 

WiFiClient client;
HTTPClient httpClient;
//*****************************************************************************************//
void setup() {
    pinMode(LED, OUTPUT);
    Serial.begin(9600);
    
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("Connected to the Wifi");
    
    SPI.begin(); 
    mfrc522.PCD_Init(); 
    Serial.println(F("Waiting to read Employee Card:")); 
}
//*****************************************************************************************//
void loop() {
    for (byte i = 0; i < 6; i++) key.keyByte[i] = 0xFF;
    byte block;
    byte len;
    if (!mfrc522.PICC_IsNewCardPresent()) {
        return;
    }
    if (!mfrc522.PICC_ReadCardSerial()) {
        return;
    }
    Serial.println(F("**Employee Card Detected:**"));
    byte buffer1[18];
    block = 4;
    len = 18;
    status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, 4, & key, & (mfrc522.uid));
    if (status != MFRC522::STATUS_OK) {
        Serial.print(F("Authentication failed: "));
        Serial.println(mfrc522.GetStatusCodeName(status));
        return;
    }
    status = mfrc522.MIFARE_Read(block, buffer1, & len);
    if (status != MFRC522::STATUS_OK) {
        Serial.print(F("Reading failed: "));
        Serial.println(mfrc522.GetStatusCodeName(status));
        return;
    }
    String value = "";
    for (uint8_t i = 0; i < 16; i++) {
        value += (char) buffer1[i];
    }
    value.trim();
    Serial.print(value);
    Serial.println(F("\n**End Reading**\n"));
    mfrc522.PICC_HaltA();
    mfrc522.PCD_StopCrypto1();

    String payload = "{\"user_id\": \"" + value + "\"}";
    httpClient.begin(client, URL);
    httpClient.addHeader("Content-Type", "application/json");
    int statusCode = httpClient.POST(payload);
    String content = httpClient.getString();
    httpClient.end();
    
    if (statusCode == 200){
      if (content == "cooldown initiated. try again later."){
      digitalWrite(LED, HIGH);
      delay(100);          
      digitalWrite(LED, LOW);
      delay(100);

      digitalWrite(LED, HIGH);
      delay(100);          
      digitalWrite(LED, LOW);
      delay(100);

      digitalWrite(LED, HIGH);
      delay(100);          
      digitalWrite(LED, LOW);
      delay(100);

      digitalWrite(LED, HIGH);
      delay(100);
      digitalWrite(LED, LOW);
      delay(100);

      digitalWrite(LED, HIGH);
      delay(100);          
      digitalWrite(LED, LOW);
      delay(100);

      digitalWrite(LED, HIGH);
      delay(100);          
      digitalWrite(LED, LOW);
      delay(100);
      }
    }
    else {
    digitalWrite(LED, HIGH);
    delay(2000);
    digitalWrite(LED, LOW);
    delay(1000);
    }
}
#include <SPI.h>
#include <Arduino.h>
#include <SPI.h>
#include <MFRC522.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define LED D1 // Led in NodeMCU at pin GPIO16 (D0).
#define RST_PIN D0 // Configurable, see typical pin layout above
#define SS_PIN D8 // Configurable, see typical pin layout above
MFRC522 mfrc522(SS_PIN, RST_PIN); // Create MFRC522 instance
MFRC522::MIFARE_Key key;
MFRC522::StatusCode status;

 
const char *WIFI_SSID = "Koders"; // Your SSID goes here
const char *WIFI_PASSWORD = "KodersKorp@12344321"; // Your wifi password goes here
const char *URL = "http://1:9020"; // Your backend link goes here

WiFiClient client;
HTTPClient httpClient;
//*****************************************************************************************//
void setup() {
    pinMode(LED, OUTPUT); // set the digital pin as output.
    Serial.begin(9600); // Initialize serial communications with the PC
    
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("Connected to the Wifi");
    
    SPI.begin(); // Init SPI bus
    mfrc522.PCD_Init(); // Init MFRC522 card
    Serial.println(F("Waiting to read personal data on a MIFARE PICC:")); //shows in serial that it is ready to read
}
//*****************************************************************************************//
void loop() {
    // Prepare key - all keys are set to FFFFFFFFFFFFh at chip delivery from the factory.
    for (byte i = 0; i < 6; i++) key.keyByte[i] = 0xFF;
    byte block;
    byte len;
    //-------------------------------------------
    // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
    if (!mfrc522.PICC_IsNewCardPresent()) {
        return;
    }
    // Select one of the cards
    if (!mfrc522.PICC_ReadCardSerial()) {
        return;
    }
    Serial.println(F("**Card Detected:**"));
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
    delay(1000);
    mfrc522.PICC_HaltA();
    mfrc522.PCD_StopCrypto1();

    String payload = "{\"user_id\": \"" + value + "\"}";
    
    httpClient.begin(client, URL);
    httpClient.addHeader("Content-Type", "application/json");
    int statusCode = httpClient.POST(payload);
    Serial.print(statusCode);
    Serial.print(payload);
    String content = httpClient.getString();
    httpClient.end();

    Serial.print(content);
    if (statusCode == 200){
      if (content == "cooldown initiated. try again later."){
      digitalWrite(LED, HIGH);// turn the LED off.(Note that LOW is the voltage level but actually
      delay(100);          // wait for 1 second.
      digitalWrite(LED, LOW);
      delay(100);

      digitalWrite(LED, HIGH);// turn the LED off.(Note that LOW is the voltage level but actually
      delay(100);          // wait for 1 second.
      digitalWrite(LED, LOW);
      delay(100);

      digitalWrite(LED, HIGH);// turn the LED off.(Note that LOW is the voltage level but actually
      delay(100);          // wait for 1 second.
      digitalWrite(LED, LOW);
      delay(100);

      digitalWrite(LED, HIGH);// turn the LED off.(Note that LOW is the voltage level but actually
      delay(100);          // wait for 1 second.
      digitalWrite(LED, LOW);
      delay(100);

      digitalWrite(LED, HIGH);// turn the LED off.(Note that LOW is the voltage level but actually
      delay(100);          // wait for 1 second.
      digitalWrite(LED, LOW);
      delay(100);

      digitalWrite(LED, HIGH);// turn the LED off.(Note that LOW is the voltage level but actually
      delay(100);          // wait for 1 second.
      digitalWrite(LED, LOW);
      delay(100);

      
      }
      else{
      digitalWrite(LED, HIGH);// turn the LED off.(Note that LOW is the voltage level but actually
      delay(2000);          // wait for 1 second.
      digitalWrite(LED, LOW);
      }
    }

    delay(1000);
}

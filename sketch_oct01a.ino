#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8); // CE, CSN

const byte address[6] = "00001";

void setup() {
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
  Serial.begin(9600);
} 

void loop() {
  if (Serial.available() > 0) {
    char input = Serial.read();  
    radio.write(&input, sizeof(input));
    Serial.println(input);  
  }

}

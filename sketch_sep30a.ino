
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8); // CE, CSN
const byte address[6] = "00001";


const int leftMotor1 = 33;
const int leftMotor2 = 32;
const int rightMotor1 = 30;
const int rightMotor2 = 31;





void setup() {
  pinMode(rightMotor1, OUTPUT);
  pinMode(leftMotor2, OUTPUT);
  pinMode(leftMotor1, OUTPUT);
  pinMode(rightMotor2, OUTPUT);
  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
}


void off() {
  digitalWrite(leftMotor1, LOW);
  digitalWrite(leftMotor2, LOW);

  digitalWrite(rightMotor1, LOW);
  digitalWrite(rightMotor2, LOW );
}

void forwards() {

  off();
  digitalWrite(leftMotor1, LOW);
  digitalWrite(leftMotor2, HIGH);

  digitalWrite(rightMotor1, HIGH);
  digitalWrite(rightMotor2, LOW);

}

void backwards() {

  off();
  digitalWrite(leftMotor1, HIGH);
  digitalWrite(leftMotor2, LOW);

  digitalWrite(rightMotor1, LOW);
  digitalWrite(rightMotor2, HIGH);  
}

void left() {

  off();
  digitalWrite(leftMotor1, HIGH);
  digitalWrite(leftMotor2, LOW);

  digitalWrite(rightMotor1, HIGH);
  digitalWrite(rightMotor2, LOW);  
}

void right() {

  off();
  delay(1);
  digitalWrite(leftMotor1, LOW);
  digitalWrite(leftMotor2, HIGH);

  digitalWrite(rightMotor1, LOW);
  digitalWrite(rightMotor2, HIGH);  
}


void loop() {

  
  if (radio.available()) {
    char text[32] = "";
    radio.read(&text, sizeof(text));
    if(strcmp(text, "f") == 0){
      forwards();
    }
    if(strcmp(text, "l") == 0){
      left();
    }
    if(strcmp(text, "r") == 0){
      right();
    }
    if(strcmp(text, "b") == 0){
      backwards();
    }
  }

}

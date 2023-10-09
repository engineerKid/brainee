
/** 
This code is for Arduino Uno - to be put on the car
  Car Feature Mappings (not case sensitive)
    R - Right Turn
    L - Left Turn
    F - Move Forward
    B - Move Backward
    S - Stop (Off)

Common Notes: 
(1) Make sure to get the latest "RF24" library version (Arduino IDE Menu >> Tools / Manage Libraries)
(2) Before uploading the sketch, make sure the port is set to the Arduino IDE (Menu >> Tools / Port)

*/

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8); // CE, CSN
const byte address[6] = "00001";

const int rightMotor1 = 30;
const int rightMotor2 = 31;
const int leftMotor2 = 32;
const int leftMotor1 = 33;

void setup() {
  pinMode(rightMotor1, OUTPUT);
  pinMode(leftMotor2, OUTPUT);
  pinMode(leftMotor1, OUTPUT);
  pinMode(rightMotor2, OUTPUT);
  
  Serial.begin(9600);
  radio.begin();  //Configuring radio receiver
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
  Serial.println("Car >> Radio started listening ");

}

void off() {
  Serial.println("Car >> turning off ");

  digitalWrite(leftMotor1, LOW);
  digitalWrite(leftMotor2, LOW);

  digitalWrite(rightMotor1, LOW);
  digitalWrite(rightMotor2, LOW );
}

void forwards() {
  Serial.println("Car >> forward");

  off();
  digitalWrite(leftMotor1, LOW);
  digitalWrite(leftMotor2, HIGH);

  digitalWrite(rightMotor1, HIGH);
  digitalWrite(rightMotor2, LOW);
}

void backwards() {
  Serial.println("Car >> backwards");
  off();
  digitalWrite(leftMotor1, HIGH);
  digitalWrite(leftMotor2, LOW);

  digitalWrite(rightMotor1, LOW);
  digitalWrite(rightMotor2, HIGH);  
}

void left() {
  Serial.println("Car >> left");
  off();
  digitalWrite(leftMotor1, HIGH);
  digitalWrite(leftMotor2, LOW);

  digitalWrite(rightMotor1, HIGH);
  digitalWrite(rightMotor2, LOW);  
}

void right() {
  Serial.println("Car >> right");
  off();
  delay(1);
  digitalWrite(leftMotor1, LOW);
  digitalWrite(leftMotor2, HIGH);

  digitalWrite(rightMotor1, LOW);
  digitalWrite(rightMotor2, HIGH);  
}

void loop() {  
  if (radio.available()) {  //radio.available() or Serial.available()
    Serial.println("Car >> Radio available");
    
    char text;
    radio.read(&text, sizeof(text));
//    text = Serial.read();
    text = tolower(text); //making the commands case insensitive
    
    if(text == 'f'){
      forwards();
    }
    else if(text == 'b'){
      backwards();
    }
    else if(text == 'l'){
      left();
    }
    else if(text == 'r'){
      right();
    }
    else if (text =='s'){
      off();
    }
  }
}

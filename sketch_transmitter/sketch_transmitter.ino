/**
 * Transmitter Code - Arduino Uno
 * 
 * Dumb transmitter
 * - Reads from the serial port
 * - Transmits that through radio 
 * - Docs on radion: https://arduinolearn.github.io/nrf1.html
 * Objective: Whoever is listening to this radio transimitter will receive the message that was sent via the Serial port) 
 */

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8); // CE, CSN
const byte address[6] = "00001";

void setup() {
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();   // set module as transmitter by setting it to not listen
  Serial.begin(9600);
} 

void loop() {
  char input;
  
//  /*****************************
//     * TEST CODE STARTS
//     * Test code without using Serial port while eeg is not ready
//     * car will move forward for few sec and then stop and go again
//     * REMOVE when attaching this to serial port
//      *************************/
//    input = 'f';  // mock data to test out
//    radio.write(&input, sizeof(input)); //By using the “&” before the variable name we actually set an indicating of the variable that stores the data that we want to be sent and using the second argument we set the number of bytes that we want to take from that variable.
//    
//    delay(1000);
//    input = 's';
//    delay(1000);
//    input = 'r';
//    delay(1000);
//    input = 'l';
//    delay(1000);
//    input = 's';  
//
//    /*********************
//     * TEST CODE ENDS
//     *********************/

  // Reading from the Serial port and transmitting    
  if (Serial.available() > 0) {
    input = Serial.read();  
    radio.write(&input, sizeof(input)); //By using the “&” before the variable name we actually set an indicating of the variable that stores the data that we want to be sent and using the second argument we set the number of bytes that we want to take from that variable.
    Serial.println(input);  
  }
}

#include <LiquidCrystal.h>

#include <boarddefs.h>
#include <IRremote.h>
#include <IRremoteInt.h>
#include <ir_Lego_PF_BitStreamEncoder.h>

IRsend irsend;

void setup() {

  Serial.begin(9600);

}

void loop() {

  if(Serial.read() == 'n'){
    irsend.sendNEC(0x213CAC53,32);

  }
  else if(Serial.read() == 'p'){
    irsend.sendNEC(0x213CEC13,32);   
  }
}

#include <LiquidCrystal.h>
const int rs = 13, en = 12, d4 = 11, d5 = 10, d6 = 9, d7 = 8;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
#include <SimpleDHT.h>
int pinDHT11 = 2;
SimpleDHT11 dht11(pinDHT11);

#define ANALOG_IN_PIN A5
float adc_voltage = 0.0;
float in_voltage = 0.0;
 
float R1 = 30000.0;
float R2 = 7500.0; 
 
float ref_voltage = 5.0;
int adc_value = 0;
 int dummy=0;

void setup() 
{
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.clear();lcd.print("SMART CROP");
  lcd.setCursor(0,1);lcd.print("MONITORING SYSTEM");
}

void loop()
{
  
   byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) 
  {
   // Serial.print("Read DHT11 failed, err="); Serial.print(SimpleDHTErrCode(err));
   // Serial.print(","); Serial.println(SimpleDHTErrDuration(err)); delay(1000);
    return;
  }
 int temp=((int)temperature);
 int hum=((int)humidity);delay(150);
 lcd.clear();lcd.print("Temp:");lcd.print(temp);lcd.print(" Hum:");lcd.print(hum);delay(100);
 int soil=analogRead(A4);delay(10);soil=1024-soil;soil=soil/10;delay(100);
 if(soil>100)
 soil=100;
 lcd.setCursor(0,1);lcd.print("Soil:");lcd.print(soil);delay(10);
float vol=0;
float vol1=0;
 int i=0;
 for(i=0;i<=10;i++)
 {
 // Read the Analog Input
  vol = analogRead(ANALOG_IN_PIN);
  if(vol>0)
  {
    vol1=vol;
  lcd.setCursor(6,1);lcd.print(" Wind:");lcd.print(vol1);delay(100);
  }
 }
  String iot=String(temp)+"&field2="+String(hum)+"&field3="+String(soil)+"&field4="+String(vol1);delay(100);
  dummy=dummy+1;delay(10);
  if(dummy>=10)
  {
  Serial.print(iot);dummy=0;
  }
}
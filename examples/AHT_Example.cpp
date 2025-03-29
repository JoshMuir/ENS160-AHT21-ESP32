#include "Arduino.h"
#include "ENS160.h"
#include "AHTxx.h"


float ahtValue;                               //to store T/RH result

AHTxx aht21(AHTXX_ADDRESS_X38, AHT2x_SENSOR); //sensor address, sensor type
void setup() 
{
    Serial.begin(115200);
    delay(1000);
    

    while (aht21.begin(27U, 26U) != true)
    {
      Serial.println(F("AHT2x not connected or fail to load calibration coefficient")); //(F()) save string to flash & keeps dynamic memory free
  
      delay(5000);
    }
    Serial.println("Setup complete");

    // Read data from AHTxx
    float humidity = aht21.readHumidity();
    float temperature = aht21.readTemperature();
    
    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.print("%, Temperature: ");
    Serial.print(temperature);
    Serial.println("°C");
}

void loop() 
{
  // put your main code here, to run repeatedly:
  delay(1000);
}
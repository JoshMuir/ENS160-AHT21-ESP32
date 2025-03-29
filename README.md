# Overview
This project implements a driver for the ENS160 air quality sensor paired with the AHT21 temperature and humidity sensor using ESP32. The implementation uses ESP-IDF v5.3.2 with Arduino as a component.

## Setup Instructions

### Prerequisites
- ESP-IDF v5.3.2
- Arduino as a component
- ESP32 development board
- ENS160+AHT21 sensor module

### Hardware Connections
Connect the ENS160+AHT21 sensor to your ESP32 board:
- VCC to 3.3V
- GND to GND
- SDA to GPIO27 
- SCL to GPIO26

### Software Setup
1. Install ESP-IDF v5.3.2 following the official documentation
2. Add Arduino as a component to your ESP-IDF project
3. Configure the project:
    - Navigate to "Component config" → "Arduino Configuration" and enable Arduino support
4. Build and flash the project

## Project Structure
- `main` - Contains main application code
- `components` - Custom components and libraries
- `managed_components` - Automatically managed components
- `build` - Build output directory


## Startup and Calibration
(Ref: https://www.reddit.com/r/arduino/comments/12ulwo2/has_anyone_been_able_to_get_ens160aht21_working/)


The ENS160 needs to be powered on for one hour for the initial startup calibration to happen but it needs to be continuously powered for 24 hours for that calibration to persist (writen to the onboard non-volatile memory).

After the initial 24 hour calibration, then it should take about 3 minutes to startup. Ref the datasheet https://www.sciosense.com/wp-content/uploads/2023/12/ENS160-Datasheet.pdf
Temperature

It is also worth mentioning that this sensor module is made from two differend sensors, the ENS160 and the ATH21, on the same device.

The ENS160 is a sensor that requires a certain heating to work, and it will heat itself up to the desired temperature. This can cause the temperature reading as measured by the ATH21 to be a few degrees higher than the ambient temperature. If your intention is to use the ENS160+ATH21 as a temperature sensor, then factor in a possible offset. 


## Usage
After flashing the firmware, the ESP32 will initialize the I2C communication with the ENS160 and AHT21 sensors. The sensors will then periodically collect:

- Air quality measurements (ENS160)
  - eCO2 (equivalent CO2)
  - TVOC (Total Volatile Organic Compounds)
  - AQI (Air Quality Index)
- Temperature and humidity (AHT21)

Measurement data is processed and output through the serial monitor at regular intervals.



## Troubleshooting
- **Sensor not detected**: Check I2C wiring and address settings
- **Invalid readings**: Ensure proper temperature calibration for the ENS160
- **Build errors**: Verify ESP-IDF version and Arduino component installation

## Discussion

The ESP-IDF is a great SDK that you must use if you want to take full advantage of the ESP32.
Arduino is also a great prototyping platform, however it can be quite limiting when it comes to utilising the ESP32. I have converted some public Arduino libraries to ESP-IDF components, and integrated them into an example project.

I hope this project helps anyone else who has found this product and is struggling to find useful implementation examples.

## References
- [ESP-IDF Programming Guide](https://docs.espressif.com/projects/esp-idf/en/latest/)
- [Arduino-ESP32 GitHub Repository](https://github.com/espressif/arduino-esp32)
- [ens16x-arduino Github Repository](https://github.com/sciosense/ens16x-arduino)
- [AHTxx-arduino Github Repository](https://github.com/enjoyneering/AHTxx)
- [Product Link](https://www.aliexpress.com/item/1005008693865239.html)
- [ENS160 Datasheet](https://www.sciosense.com/wp-content/uploads/2023/12/ENS160-Datasheet.pdf)
- [AHT21 Datasheet](http://www.aosong.com/userfiles/files/media/AHT21%E4%BA%A7%E5%93%81%E8%A7%84%E6%A0%BC%E4%B9%A6(%E8%8B%B1%E6%96%87%E7%89%88)%20A3.pdf)



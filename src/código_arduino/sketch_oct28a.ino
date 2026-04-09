#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <DHT.h>

#define DHTPIN 2       
#define DHTTYPE DHT11  
DHT dht(DHTPIN, DHTTYPE);

Adafruit_BMP280 bmp; 

void setup() {
  Serial.begin(9600);
  
  dht.begin();
  Serial.println("Arduino ligou! Iniciando sensores...");

  unsigned status = bmp.begin(0x77); 
  if (!status) {
    Serial.println("{\"erro\": \"BMP280 nao encontrado. Verifique as conexoes ou o endereco I2C!\"}");
    while (1) delay(10); 
  }

  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     
                  Adafruit_BMP280::SAMPLING_X2,     
                  Adafruit_BMP280::SAMPLING_X16,    
                  Adafruit_BMP280::FILTER_X16,      
                  Adafruit_BMP280::STANDBY_MS_500); 
}

void loop() {
  delay(5000); 

  float umidade = dht.readHumidity();
  float temperaturaDHT = dht.readTemperature();

  float pressao = bmp.readPressure() / 100.0F; 

  if (isnan(umidade) || isnan(temperaturaDHT)) {
    Serial.println("{\"erro\": \"Falha na leitura do sensor DHT11\"}");
    return;
  }

  Serial.print("{");
  Serial.print("\"temperatura\": ");
  Serial.print(temperaturaDHT);
  Serial.print(", \"umidade\": ");
  Serial.print(umidade);
  Serial.print(", \"pressao\": ");
  Serial.print(pressao);
  Serial.println("}"); 
}

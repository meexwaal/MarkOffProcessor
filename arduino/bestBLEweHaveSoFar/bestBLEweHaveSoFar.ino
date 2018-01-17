
#include <Arduino.h>
#include <bluefruit.h>

// the best description of what I've done that my 1:30am brain can manage
// in terminal,
// sudo hciconfig hci0 up
// sudo gatttool -b D6:88:F3:AA:42:29 -I -t random --sec-level=high
// Then in the gatttool prompt,
// connect
// primary
// char-desc
// char-read-uuid 2902 # probably?
// char-write-req 0x000b 0300 # This "enables notifications" or something. 
// This is enough to get reading from arduino


// BLE Service
BLEDis  bledis;
BLEUart bleuart;

void setup()
{
  Serial.begin(115200);
  Serial.println("Adafruit Bluefruit Neopixel Test");
  Serial.println("--------------------------------");

  Serial.println();
  Serial.println("Please connect using the Bluefruit Connect LE application");

  // Init Bluefruit
  Bluefruit.begin();
  // Set max power. Accepted values are: -40, -30, -20, -16, -12, -8, -4, 0, 4
  Bluefruit.setTxPower(4);
  Bluefruit.setName("Bluefruit52");
  Bluefruit.setConnectCallback(connect_callback);

  // Configure and Start Device Information Service
  bledis.setManufacturer("Adafruit Industries");
  bledis.setModel("Bluefruit Feather52");
  bledis.begin();

  // Configure and start BLE UART service
  bleuart.begin();

  // Set up and start advertising
  startAdv();
}

void startAdv(void)
{
  // Advertising packet
  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();

  // Include bleuart 128-bit uuid
  Bluefruit.Advertising.addService(bleuart);

  // Secondary Scan Response packet (optional)
  // Since there is no room for 'Name' in Advertising packet
  Bluefruit.ScanResponse.addName();

  /* Start Advertising
     - Enable auto advertising if disconnected
     - Interval:  fast mode = 20 ms, slow mode = 152.5 ms
     - Timeout for fast mode is 30 seconds
     - Start(timeout) with timeout = 0 will advertise forever (until connected)

     For recommended advertising interval
     https://developer.apple.com/library/content/qa/qa1931/_index.html
  */
  Bluefruit.Advertising.restartOnDisconnect(true);
  Bluefruit.Advertising.setInterval(32, 244);    // in unit of 0.625 ms
  Bluefruit.Advertising.setFastTimeout(30);      // number of seconds in fast mode
  Bluefruit.Advertising.start(0);                // 0 = Don't stop advertising after n seconds
}

void connect_callback(uint16_t conn_handle)
{
  char central_name[32] = { 0 };
  Bluefruit.Gap.getPeerName(conn_handle, central_name, sizeof(central_name));

  Serial.print("Connected to ");
  Serial.println(central_name);

  Serial.println("Please select the 'Neopixels' tab, click 'Connect' and have fun");
}

void loop()
{
  //bleuart.write(65);
  // Echo received data
  if ( Bluefruit.connected() && bleuart.notifyEnabled() )
  {
    //bleuart.write(66);
    int command = bleuart.read();
    if (command != -1)
      Serial.print(command);

    switch (command) {
      case 'V': {   // Get Version
          digitalWrite(17, HIGH);
          break;
        }

      case 'S': {   // Setup dimensions, components, stride...
          digitalWrite(17, LOW);
          break;
        }


    }
  }
}


void sendResponse(char const *response) {
  Serial.printf("Send Response: %s\n", response);
  bleuart.write(response, strlen(response)*sizeof(char));
}


// String is_on;

int button_in = 2;
int led_out = 3;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(button_in, INPUT);
  pinMode(led_out, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  // int pressed = digitalRead(button_in);
  Serial.println('Hello');
  // if (Serial.available()) {
  //   is_on = Serial.readStringUntil('\n');
  //   is_on.trim();
  //   if (is_on.equals("0")){
  //     digitalWrite(led_out, HIGH);
  //   } else {
  //     digitalWrite(led_out, LOW);
  //   }
  // }
  delay(3000);
}

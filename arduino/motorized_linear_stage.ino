// 200 steps per revolution with a pitch of 1mm
// 10000 steps for 50 mm

class Motor
{
  public:
    Motor(const int stepPin, const int dirPin, const int enablePin)
      : stepPin(stepPin), dirPin(dirPin), enablePin(enablePin)
    {
    }

    void begin()
    {
      pinMode(stepPin, OUTPUT);
      pinMode(dirPin, OUTPUT);
      pinMode(enablePin, OUTPUT);
      digitalWrite(stepPin, LOW);
      digitalWrite(dirPin, LOW);
      digitalWrite(enablePin, HIGH);
    }

    void enable(const bool ENABLE)
    {
      if (ENABLE)
        digitalWrite (enablePin, LOW);
      else
        digitalWrite (enablePin, HIGH);
    }

    void set_dt(const int dt){
     this->dt = dt;
    }

    void get_X()
    {
      Serial.println(X);
    }

    void zero()
    {
      X = 0;
    }

    void move(const long NX)
    {
      if ( !digitalRead(enablePin) ){

        long xt;

        // determine motion direction
        if (NX>X) {
          xt = NX-X;
          digitalWrite (dirPin,LOW);
          xt=1;
        } else {
          xt = X-NX;
          digitalWrite (dirPin,HIGH);
          xt=-1;
        }

        for (; X !=NX; X=X+xt) {
          // check for serial commands
          if (Serial.available() > 0) {
            char c = Serial.read();
            if (c == '0')
              break;
            if (c == 'q')
              this->get_X();
          }

          // execute the motion
          digitalWrite (stepPin, HIGH);
          delayMicroseconds (dt);
          digitalWrite (stepPin, LOW);
          delayMicroseconds (dt);
        }
        enable(0);
      }
  }

  private:
    long X = 0;    // present position
    int dt = 500;  // step duration

    const int stepPin, dirPin, enablePin;
};

Motor motor_x(2,5,8);
void setup()
{
  Serial.begin(9600);

  motor_x.begin();
}

void serialEvent()
{
  while (Serial.available() > 0) {
    char cmd = Serial.read();
    switch (cmd) {
      case 'e':
        motor_x.enable(Serial.parseInt());
        break;

      case 's':
        motor_x.set_dt(Serial.parseInt());
        break;

      case 'm':
        motor_x.move(Serial.parseInt());
        break;

      case 'x':
        motor_x.get_X();
        break;

      case 'z':
        motor_x.zero();
        break;

      case 'q':
        Serial.println("Not moving.");
        break;

      case '?':
        Serial.println("CeNTREX motorized linear stage V1.0");
        break;
    }
  }
}

void loop()
{
}
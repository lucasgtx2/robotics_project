// Arduino Solenoid Activation Code
#include <Arduino.h>
#include <LinkedList.h>

// Global variables
String musica;

int mapCharToConstant(char note);
void splitStringAndAppendToList(const String &inputString, char separator, LinkedList<String> &outputList);

// Arduino setup
void setup() {
  Serial.begin(9600);

  for (int i = 2; i < 14; i++) {
    pinMode(i, OUTPUT);
  }
}

void loop() {
  //while (!Serial.available());
  musica = Serial.readString();

  LinkedList<String> resultList;

  // Split the string and append to the list
  splitStringAndAppendToList(musica, '|', resultList);

  // Print the result
  Serial.println("Result List:");
  for (int i = 0; i < resultList.size(); i++) {
    Serial.println(resultList.get(i));
  }

  for(int i = 0; i < resultList.size(); i++){
    String chord = resultList.get(i);
    String notes = chord.substring(chord.indexOf("S") + 1, chord.indexOf("T"));
    unsigned long tempo = chord.substring(chord.indexOf("T") + 1, chord.indexOf("Z")).toInt();
  
    // Activate solenoids
    if (notes.charAt(0) != 'P') {
      for (int j = 0; j < notes.length(); j++) {
        int mappedValue = mapCharToConstant(notes.charAt(j));
        digitalWrite(mappedValue, HIGH); // Activate solenoid
        Serial.println(mappedValue);
      }
  
      delay(tempo);
      Serial.println(tempo);
  
      // Turn off solenoids
      for (int j = 0; j < notes.length(); j++) {
        int mappedValue = mapCharToConstant(notes.charAt(j));
        digitalWrite(mappedValue, LOW); // Turn off solenoid
      }
    } else {
      delay(tempo);
    }
  }
  delay(5);
}

// Function to map a character to a constant integer
int mapCharToConstant(char note) {
  switch (note) {
    case 'C':
      return 2;
    case 'D':
      return 3;
    case 'E':
      return 4;
    case 'F':
      return 10;
    case 'G':
      return 11;
    case 'A':
      return 12;
    case 'B':
      return 13;
    case 'J':
      return 9;
    case 'K':
      return 8;
    case 'L':
      return 7;
    case 'M':
      return 6;
    case 'N':
      return 5;
    default:
      // Return an invalid value or handle the case as needed
      return -1;
  }
}

void splitStringAndAppendToList(const String &inputString, char separator, LinkedList<String> &outputList) {
  int separatorIndex = 0;
  int lastIndex = 0;

  while ((separatorIndex = inputString.indexOf(separator, lastIndex)) != -1) {
    // Extract substring between lastIndex and separatorIndex
    String substring = inputString.substring(lastIndex, separatorIndex);

    // Append substring to the list
    outputList.add(substring);

    // Update lastIndex to the character after the separator
    lastIndex = separatorIndex + 1;
  }

  // Append the last substring (after the last separator) to the list
  String lastSubstring = inputString.substring(lastIndex);
  outputList.add(lastSubstring);
}
// Código de ativação das solenides Arduino

// Bibliotecas

// Declaração de variáveis globais
String musica;
StringArray lista_acordes;

const int C = 8;
const int D = 7;
const int E = 6;
const int F = 5;
const int G = 3;
const int A = 4;
const int B = 9;
const int J = 13; //C#
const int K = 12; //D#
const int L = 11; //F#
const int M = 10; //G#
const int N = 2;  //A#

// Configurações do Arduino
void setup() {
  Serial.begin(115200);

  pinMode(C, OUTPUT);
  pinMode(D, OUTPUT);
  pinMode(E, OUTPUT);
  pinMode(F, OUTPUT);
  pinMode(G, OUTPUT);
  pinMode(A, OUTPUT);
  pinMode(B, OUTPUT);
  pinMode(J, OUTPUT);
  pinMode(K, OUTPUT);
  pinMode(L, OUTPUT);
  pinMode(M, OUTPUT);
  pinMode(N, OUTPUT);
}

void loop() {
  // Leitura da Serial
  while (!Serial.available());
  musica = Serial.readString();
  Serial.print(musica);

  // Cria lista de acordes
  lista_acordes = musica.split('|');

  // Tocar música completa
  int numAcordes = sizeof(lista_acordes);
  for (int i=0; i<numAcordes; i++) {

    // Obtenção da sequência de notas e tempos
    String acorde = lista_acordes(i);
    String notas = acorde.substring(acorde.indexof("S")+1,acorde.indexof("T"));
    int tempo = acorde.substring(acorde.indexof("T")+1,acorde.indexof("E"));
    Serial.print(acorde);

    // Aciona solenoides
    if (notas(0) != "P"){
      for (int i=0; i<sizeof(notas); i++) {
        //digitalWrite(notas(i), HIGH);
        Serial.print(notas(i));
      }

      delay(tempo);

      // Desliga solenoides
      for (int i=0; i<sizeof(notas); i++) {
        //digitalWrite(notas(i), LOW);
        Serial.print(notas(i));
      }
    } else {
      delay(tempo);
    }
  }
}

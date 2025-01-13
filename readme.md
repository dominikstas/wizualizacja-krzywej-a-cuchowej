# Dominik Stasiak
# Fizyka Techniczna - semestr 1

# Wizualizacja Krzywej Łańcuchowej  

## Opis projektu  
Program służy do wizualizacji krzywej łańcuchowej (catenary curve) w formie wykresu. Użytkownik może wprowadzić parametry takie jak odległość między podporami, wysokość podpór, długość łańcucha oraz wagę liny, aby wygenerować wykres krzywej oraz  wyświetlić jej równanie.

## Teoria  
Krzywa łańcuchowa opisuje kształt, jaki przybiera lina lub łańcuch zawieszony na dwóch podporach, pod wpływem swojego ciężaru. Kształt ten można matematycznie wyrazić za pomocą funkcji hiperbolicznej cosinus:  

y = a * cosh((x - L/2) / a) - a * cosh(L / (2a)) + h


gdzie:  
- \(a\) - parametr krzywej zależny od długości łańcucha i odległości między podporami,  
- \(L\) - odległość między podporami,  
- \(h\) - wysokość podpór.  

Krzywa ta ma szerokie zastosowanie w inżynierii, na przykład w projektowaniu mostów i przewodów.

## Wykorzystane biblioteki  
- **`tkinter`**  
  - Moduł użyty do stworzenia interfejsu graficznego.  

- **`numpy`**  
  - Biblioteka użyta do obliczeń matematycznych.  


- **`matplotlib`**  
  - Biblioteka do tworzenia wykresów.  





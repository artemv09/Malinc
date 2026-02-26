#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

int main() {
    FILE *inputFile, *outputFile;
    char line[1024];
    double number;
    
    // Открываем файлы
    inputFile = fopen("volt_1.txt", "r");
    if (inputFile == NULL) {
        printf("Ошибка открытия файла volt_1.txt\n");
        return 1;
    }
    
    outputFile = fopen("abc_ln.txt", "w");
    if (outputFile == NULL) {
        printf("Ошибка создания выходного файла\n");
        fclose(inputFile);
        return 1;
    }
    
    // Читаем числа и записываем их логарифмы
    while (fgets(line, sizeof(line), inputFile) != NULL) {
        // Удаляем символ новой строки, если он есть
        size_t len = strlen(line);
        if (len > 0 && line[len-1] == '\n') {
            line[len-1] = '\0';
        }
        
        // Пропускаем пустые строки
        if (strlen(line) == 0) {
            continue;
        }
        
        // Преобразуем строку в число (строка может содержать запятую)
        // Заменяем запятую на точку для atof()
        for (int i = 0; line[i] != '\0'; i++) {
            if (line[i] == ',') {
                line[i] = '.';
            }
        }
        
        number = atof(line);
        
        // Проверяем, что число положительное
        if (number > 0) {
            double logValue = log(number);
            
            // Создаём строку с логарифмом и меняем точку на запятую
            char buffer[50];
            sprintf(buffer, "%f", logValue);
            
            // Меняем точку на запятую
            for (int i = 0; buffer[i] != '\0'; i++) {
                if (buffer[i] == '.') {
                    buffer[i] = ',';
                }
            }
            
            fprintf(outputFile, "%s\n", buffer);
        } else {
            fprintf(outputFile, "NaN\n"); // Not a Number для x <= 0
        }
    }
    
    printf("Готово! Результат в файле abc_ln.txt\n");
    
    fclose(inputFile);
    fclose(outputFile);
    return 0;
}
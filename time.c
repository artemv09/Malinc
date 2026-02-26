#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    FILE *inputFile, *outputFile;
    char line[1024];
    char *inputFilename = "abc.txt";
    char *outputFilename = "time_1.txt";
    int lineCount = 0;
    int numberCount = 0;
    
    inputFile = fopen(inputFilename, "r");
    if (inputFile == NULL) {
        printf("Ошибка: не удалось открыть файл %s\n", inputFilename);
        return 1;
    }
    
    outputFile = fopen(outputFilename, "w");
    if (outputFile == NULL) {
        printf("Ошибка: не удалось создать файл %s\n", outputFilename);
        fclose(inputFile);
        return 1;
    }
    
    printf("Обработка файла %s...\n", inputFilename);
    
    while (fgets(line, sizeof(line), inputFile) != NULL) {
        lineCount++;
        
        size_t len = strlen(line);
        if (len > 0 && line[len-1] == '\n') {
            line[len-1] = '\0';
        }
        
        if (strlen(line) == 0) continue;
        
        // Ищем запятую
        char *commaPos = strchr(line, ',');
        if (commaPos != NULL) {
            *commaPos = '\0';
        }
        
        // Преобразуем в число
        char *endptr;
        double number = strtod(line, &endptr);
        
        if (endptr != line) {
            numberCount++;
            
            // === СОЗДАЁМ СТРОКУ С ЧИСЛОМ И МЕНЯЕМ ТОЧКУ НА ЗАПЯТУЮ ===
            char buffer[50];  // Достаточно для числа
            sprintf(buffer, "%f", number);  // Записываем число в строку (с точкой)
            
            // Меняем точку на запятую
            for (int i = 0; buffer[i] != '\0'; i++) {
                if (buffer[i] == '.') {
                    buffer[i] = ',';
                }
            }
            
            // Записываем в файл с запятой
            fprintf(outputFile, "%s\n", buffer);
            printf("  Записано число %d: %s\n", numberCount, buffer);
        } else {
            printf("  Предупреждение: не удалось преобразовать '%s' в число\n", line);
        }
    }
    
    printf("\nОбработка завершена!\n");
    printf("Всего обработано строк: %d\n", lineCount);
    printf("Найдено и записано чисел: %d\n", numberCount);
    printf("Результат сохранен в файл: %s\n", outputFilename);
    
    fclose(inputFile);
    fclose(outputFile);
    
    return 0;
}
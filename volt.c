#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    FILE *inputFile, *outputFile;
    char line[1024];
    char *inputFilename = "abc.txt";
    char *outputFilename = "volt_1.txt";
    int lineCount = 0;
    int numberCount = 0;
    
    // Открываем исходный файл для чтения
    inputFile = fopen(inputFilename, "r");
    if (inputFile == NULL) {
        printf("Ошибка: не удалось открыть файл %s\n", inputFilename);
        return 1;
    }
    
    // Открываем выходной файл для записи
    outputFile = fopen(outputFilename, "w");
    if (outputFile == NULL) {
        printf("Ошибка: не удалось создать файл %s\n", outputFilename);
        fclose(inputFile);
        return 1;
    }
    
    printf("Обработка файла %s...\n", inputFilename);
    printf("Удаляем числа до запятой и оставляем числа после запятой\n");
    printf("--------------------------------------------------------\n");
    
    // Читаем файл построчно до конца
    while (fgets(line, sizeof(line), inputFile) != NULL) {
        lineCount++;
        
        // Удаляем символ новой строки, если он есть
        size_t len = strlen(line);
        if (len > 0 && line[len-1] == '\n') {
            line[len-1] = '\0';
        }
        
        // Пропускаем пустые строки
        if (strlen(line) == 0) {
            continue;
        }
        
        printf("Строка %d: '%s'\n", lineCount, line);
        
        // Ищем запятую в строке
        char *commaPos = strchr(line, ',');
        
        if (commaPos != NULL) {
            // Нашли запятую - берем все что после нее
            char *afterComma = commaPos + 1;
            
            // Пропускаем пробелы после запятой, если они есть
            while (*afterComma == ' ' || *afterComma == '\t') {
                afterComma++;
            }
            
            // Преобразуем оставшуюся часть в число
            char *endptr;
            double number = strtod(afterComma, &endptr);
            
            // Проверяем, что преобразование прошло успешно
            if (endptr != afterComma) {
                numberCount++;
                
                // === СОЗДАЁМ СТРОКУ С ЧИСЛОМ И МЕНЯЕМ ТОЧКУ НА ЗАПЯТУЮ ===
                char buffer[50];
                sprintf(buffer, "%f", number);
                
                // Меняем точку на запятую
                for (int i = 0; buffer[i] != '\0'; i++) {
                    if (buffer[i] == '.') {
                        buffer[i] = ',';
                    }
                }
                
                // Записываем в файл с запятой
                fprintf(outputFile, "%s\n", buffer);
                printf("  → Найдено число после запятой: %s (записано с запятой)\n", buffer);
            } else {
                printf("  → Ошибка: после запятой нет числа\n");
            }
        } else {
            printf("  → Нет запятой в строке, строка пропущена\n");
        }
    }
    
    printf("\n--------------------------------------------------------\n");
    printf("Обработка завершена!\n");
    printf("Всего обработано строк: %d\n", lineCount);
    printf("Сохранено чисел в %s: %d\n", outputFilename, numberCount);
    
    // Закрываем файлы
    fclose(inputFile);
    fclose(outputFile);
    
    return 0;
}
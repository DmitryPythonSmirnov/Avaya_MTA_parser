### Avaya MTA parser

Скрипт парсит файл MTA-файл (файл, полученный с помощью MTA (Message Trace Analyzer)
из MST (Message Sequence Trace)) от станции Avaya для вызовов по SIP-транку.

Исходный файл MTA должен находиться в том же каталоге, что и скрипт. При запуске скрипт выводит список всех файлов в текущем каталоге и предлагает выбрать файл для парсинга. MTA-файл может быть большим, скрипт не загружает его в память, а читает построчно. При парсинге в основном расходуются ресурсы процессора, а не памяти.

Запуск осуществляется следующим образом:

`python avaya_mta_parser.py`

или двойным кликом, или другим аналогичным способом, в зависимости от настроек операционной системы.

Скрипт запрашивает номер телефона (можно ввести часть номера) вызывающего абонента (From) или Call-ID вызова. Если введён номер телефона, то будет найден только первый вызов в файле
с этим номером (скрипт сам найдёт Call-ID этого вызова). Все найденные SIP-сообщения с соответствующим Call-ID сохраняются в файл "result.txt" в текущем каталоге.

---

**Требования:**  
Python версии 3.6 и выше.  
Скрипт не требует никаких дополнительных библиотек.
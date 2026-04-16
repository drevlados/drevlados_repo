#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <random>
#include <format>
#include <fstream>

using namespace std;

class Table;
class DB
{
private:
    map<string, Table*> tables; //хранилище таблиц по именам

public:
    void addTable(const string& name, const vector<string>& header);
    Table* getTable(const string& name);
    ~DB();
};

class Table
{
private:
    vector<string> header;                  //заголовок
    vector<vector<string>> data;            //данные
    string name;                            //имя таблицы

    //структура для индексов
    map<string, pair<int, multimap<string, size_t>>> indexes;

public:
    //создание таблицы с именем и заголовком
    Table(const string& tableName, const vector<string>& tableHeader);
    void addData(const vector<string>& row);                    //добавление строки данных
    void print();                                               //вывод таблицы на экран
    Table* select(const string& column, const string& value);   // поиск данных по условию

    //
    void addIndex(const string& column);
};

//добавление таблицы
void DB::addTable(const string& name, const vector<string>& header) {
    tables[name] = new Table(name, header);
}
//получение таблицы
Table* DB::getTable(const string& name) {
    if (tables.find(name) != tables.end()) {
        return tables[name];
    }
    return nullptr;
}
//деструктор
DB::~DB() {
    for (auto& pair : tables) {
        delete pair.second;
    }
}

// Реализация методов Table
Table::Table(const string& tableName, const vector<string>& tableHeader)
    : name(tableName), header(tableHeader) {
}

//добавление строки данных
void Table::addData(const vector<string>& row) {
    if (row.size() == header.size()) {
        data.push_back(row);
        size_t newRowIndex = data.size() - 1;

        for (auto& kv : indexes) {
            int colIndex = kv.second.first;
            auto& mmap = kv.second.second;
            mmap.insert({ row[colIndex], newRowIndex });
        }
    }
}

void Table::addIndex(const string& column) {
    int columnIndex = -1;
    for (size_t i = 0; i < header.size(); ++i) {
        if (header[i] == column) {
            columnIndex = static_cast<int>(i);
            break;
        }
    }
    if (columnIndex == -1) {
        return;
    }

    multimap<string, size_t> idx;

    for (size_t rowIdx = 0; rowIdx < data.size(); ++rowIdx) {
        idx.insert({ data[rowIdx][columnIndex], rowIdx });
    }
    indexes[column] = { columnIndex, std::move(idx) };
}

//вывод таблицы
void Table::print() {
    for (const auto& col : header) {
        cout << col << "\t";
    }
    cout << "\n-------------------\n";
    //вывод данных
    for (const auto& row : data) {
        for (const auto& cell : row) {
            cout << cell << "\t";
        }
        cout << endl;
    }
    cout << endl;
}

//выборка данных
Table* Table::select(const string& column, const string& value) {
    //поиск индекса столбца
    //Новый
    auto itIndex = indexes.find(column);
    if (itIndex != indexes.end()) {
        int colIndex = itIndex->second.first;
        auto& mmap = itIndex->second.second;

        Table* resultTable = new Table("result", header);

        auto range = mmap.equal_range(value);
        for (auto it = range.first; it != range.second; ++it) {
            size_t rowIdx = it->second;                    // номер строки
            resultTable->addData(data[rowIdx]);            // добавляем строку
        }
        return resultTable;
    }

    //Старый
    int columnIndex = -1;
    for (size_t i = 0; i < header.size(); i++) {
        if (header[i] == column) {
            columnIndex = i;
            break;
        }
    }
    if (columnIndex == -1) {
        return new Table("result", header);
    }
    //таблица для результатов
    Table* resultTable = new Table("result", header);
    //поиск подходящих строк
    for (size_t i = 0; i < data.size(); i++) {
        const auto& row = data[i];
        if (row[columnIndex] == value) {
            resultTable->addData(row);
        }
    }
    return resultTable;
}



int main()
{
    setlocale(LC_ALL, "Rus");
    DB db;
    clock_t start, finish;
    double duration;
    ofstream F;
    // Добавление таблицы. Вариант 2. На основе std::vector
    vector<string> header_2;
    header_2.push_back("1");
    header_2.push_back("2");
    header_2.push_back("3");
    db.addTable("T_2", header_2);

    Table* t2 = db.getTable("T_2");
    vector<string> data;
    srand(time(0));
    string str_num ;
    int lines = 10;
    int obl_znach = 100;

    //индексирование столбца 1
    t2->addIndex("1");
    start = clock();
    F.open("results_with_index.txt", ios::out);
    //Значение времени с индексацией
    while (lines < 150000){
        for (int i = 0; i < lines; i++) {
            data.push_back(str_num = to_string(rand()%obl_znach));
            data.push_back(str_num = to_string(rand()%obl_znach));
            data.push_back(str_num = to_string(rand()%obl_znach));
            t2->addData(data);
            data.clear();
        }
        t2->addIndex("1");
        start = clock();
        Table* result_2 = t2->select("1", str_num = to_string(rand()%obl_znach));
        delete result_2;
        finish = clock();
        duration = (double)(finish - start) / CLOCKS_PER_SEC*100;
        F << duration;
        F << '\n';
        lines = lines * 2;
    }
    F.close();
    F.open("results_with_no_index.txt", ios::out);
    lines = 10;
    //Значение времени без индексации
    while (lines < 150000){
        for (int i = 0; i < lines; i++) {
            data.push_back(str_num = to_string(rand()%obl_znach));
            data.push_back(str_num = to_string(rand()%obl_znach));
            data.push_back(str_num = to_string(rand()%obl_znach));
            t2->addData(data);
            data.clear();
        }
        start = clock();
        Table* result_2 = t2->select("1", str_num = to_string(rand()%obl_znach));
        delete result_2;
        finish = clock();
        duration = (double)(finish - start) / CLOCKS_PER_SEC*100;
        F << duration;
        F << '\n';
        lines = lines * 2;
    }
    F.close();
    
    //работает, но какие-то траблы с маком???
    system("python3 /Users/vladislav/прога/плюсы/лабы№3_4_5/skript.py");
    return 0;
}

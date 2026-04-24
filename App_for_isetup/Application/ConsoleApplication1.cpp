#include <iostream>
#include <string>
#include <vector>
#include <map>

using namespace std;

class Table;

/*!
 * \brief Класс простой базы данных.
 * Хранит набор таблиц по строковому имени и позволяет добавлять и получать таблицы.
 */
class DB
{
private:
    map<string, Table*> tables; ///< Хранилище таблиц по их именам.

public:
    /*!
     * \brief Добавляет новую таблицу в базу данных.
     * \param name Имя таблицы.
     * \param header Вектор с именами столбцов таблицы.
     */
    void addTable(const string& name, const vector<string>& header);

    /*!
     * \brief Возвращает указатель на таблицу по её имени.
     * \param name Имя таблицы.
     * \return Указатель на таблицу или nullptr, если таблица отсутствует.
     */
    Table* getTable(const string& name);

    /// Деструктор, освобождающий память, занятую таблицами.
    ~DB();
};

/*!
 * \brief Класс таблицы с текстовыми данными.
 *
 * Таблица хранит строковые заголовки столбцов и строки данных, а также поддерживает
 * создание индексов по столбцам для ускорения выборки.
 */
class Table
{
private:
    vector<string> header;                  /**< Заголовок таблицы: имена столбцов. */
    vector<vector<string>> data;            /**< Данные таблицы: строки и ячейки.   */
    string name;                            //!< Имя таблицы.
    map<string, pair<int, multimap<string, size_t>>> indexes; ///< Индексы по столбцам.

public:
    /*!
     * \brief Конструктор таблицы с именем и заголовком.
     * \param tableName Имя таблицы.
     * \param tableHeader Вектор строк с именами столбцов.
     */
    Table(const string& tableName, const vector<string>& tableHeader);

    /*!
     * \brief Добавляет строку данных в таблицу.
     * \param row Вектор строк, представляющий одну строку данных.
     */
    void addData(const vector<string>& row);

    /*!
     * \brief Выводит таблицу на стандартный поток вывода.
     */
    void print();

    /*!
     * \brief Выполняет выборку строк по условию «столбец = значение».
     * \param column Имя столбца, по которому выполняется поиск.
     * \param value Значение, которое должно быть в указанном столбце.
     * \return Указатель на новую таблицу с найденными строками.
     */
    Table* select(const string& column, const string& value);

    /*!
     * \brief Создаёт индекс по указанному столбцу.
     * \param column Имя столбца, по которому создаётся индекс.
     */
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
    //поиск индекса столбца (оптимизированный вариант)
    auto itIndex = indexes.find(column);
    if (itIndex != indexes.end()) {
        int colIndex = itIndex->second.first;
        auto& mmap = itIndex->second.second;

        Table* resultTable = new Table("result", header);

        auto range = mmap.equal_range(value);
        for (auto it = range.first; it != range.second; ++it) {
            size_t rowIdx = it->second;
            resultTable->addData(data[rowIdx]);
        }
        return resultTable;
    }

    //полный перебор (если индекс не найден)
    int columnIndex = -1;
    for (size_t i = 0; i < header.size(); i++) {
        if (header[i] == column) {
            columnIndex = static_cast<int>(i);
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

    vector<string> header_1{ "A", "B", "C" };
    db.addTable("T_1", header_1);

    Table* t1 = db.getTable("T_1");
    t1->addData({ "A1", "B1", "C1" });
    t1->addData({ "A2", "B2", "C2" });
    t1->addData({ "A3", "B3", "C3" });
    t1->addData({ "A1", "B10", "C10" });

    Table* result_1 = t1->select("A", "A1");
    result_1->print();
    delete result_1;

    vector<string> header_2;
    header_2.push_back("D");
    header_2.push_back("E");
    header_2.push_back("F");
    db.addTable("T_2", header_2);

    Table* t2 = db.getTable("T_2");
    vector<string> data;

    data.push_back("D1");
    data.push_back("E1");
    data.push_back("F1");
    t2->addData(data);

    data.clear();
    data.push_back("D2");
    data.push_back("E2");
    data.push_back("F2");
    t2->addData(data);

    t2->addIndex("D");

    Table* result_2 = t2->select("D", "D1");
    result_2->print();
    delete result_2;

    data.clear();
    data.push_back("D1");
    data.push_back("E3");
    data.push_back("F3");
    t2->addData(data);

    Table* result_3 = t2->select("D", "D1");
    result_3->print();
    delete result_3;

    cout << "Вся таблица Вар.1:" << endl;
    t1->print();

    cout << "Вся таблица Вар.2:" << endl;
    t2->print();

    system("pause");
    return 0;
}
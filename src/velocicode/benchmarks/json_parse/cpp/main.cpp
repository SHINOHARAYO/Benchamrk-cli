#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "json.hpp"

using json = nlohmann::json;

int main(int argc, char* argv[]) {
    int n = 1;
    if (argc > 1) {
        n = std::atoi(argv[1]);
    }

    std::string data_path = "../../data.json";
    std::ifstream f(data_path);
    if (!f.good()) {
        data_path = "data.json";
        f.open(data_path);
        if (!f.good()) {
            data_path = "../data.json";
            f.open(data_path);
        }
    }

    if (!f.good()) {
        std::cerr << "Error: data.json not found" << std::endl;
        return 1;
    }

    // Read entire file into string buffer first
    std::string str((std::istreambuf_iterator<char>(f)),
                     std::istreambuf_iterator<char>());
    f.close();

    int result_size = 0;

    for (int i = 0; i < n; ++i) {
        auto j = json::parse(str);
        if (j.is_array()) {
            result_size = j.size();
        }
    }

    if (result_size == 0) {
        // Prevent optimization (though unlikely with side effects inside library)
    }

    return 0;
}

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <regex>
#include <cstdlib>

int main(int argc, char* argv[]) {
    int n = 1;
    if (argc > 1) {
        n = std::atoi(argv[1]);
    }

    // Path to data.txt
    // Executable is in .../cpp/bin/runner_cpp
    // data.txt is in .../regex_redact/data.txt
    // We need to look up relative to the executable or source
    
    // Simple check: try "data.txt", "../data.txt", "../../data.txt"
    std::string dataPath = "data.txt";
    std::ifstream f(dataPath);
    if (!f.good()) {
        dataPath = "../data.txt";
        f.open(dataPath);
         if (!f.good()) {
            dataPath = "../../data.txt";
            f.open(dataPath);
             if (!f.good()) {
                  // Last ditch: hardcoded path relative to this source file location
                  // Not easily known at runtime without __FILE__ manipulation at compile time?
                  // Let's assume runner sets CWD or we find it nearby.
                  // For now, fail.
                  std::cerr << "Error: data.txt not found" << std::endl;
                  return 1;
             }
        }
    }
    
    // Read entire file
    std::stringstream buffer;
    buffer << f.rdbuf();
    std::string content = buffer.str();
    
    // std::regex is known to be slow, but it IS standard.
    // Try to optimize compilation
    std::regex phoneRe("\\d{3}-\\d{3}-\\d{4}", std::regex_constants::optimize);
    std::regex emailRe("[a-z]{8}@example\\.com", std::regex_constants::optimize);

    std::string result;

    for (int i = 0; i < n; ++i) {
        // regex_replace returns a new string
        std::string temp = std::regex_replace(content, phoneRe, "[PHONE]");
        result = std::regex_replace(temp, emailRe, "[EMAIL]");
    }

    if (result.length() == 0) {
        std::cerr << "Error" << std::endl;
    }

    return 0;
}

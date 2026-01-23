#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <iterations>" << std::endl;
        return 1;
    }

    int n = 1000000;
    if (argc > 1) {
        n = std::atoi(argv[1]);
    }
    std::string s = "velocicode";
    std::string result;
    
    // Optional: reserve memory to test pure concat speed vs allocation speed?
    // "Real world" often implies we don't know the size. 
    // Let's NOT reserve to test reallocation performance which is part of "String handling".
    
    for (int i = 0; i < n; ++i) {
        result += s;
    }

    // Prevent optimization
    if (result.length() == 0) {
        std::cout << "Error" << std::endl;
    }

    return 0;
}

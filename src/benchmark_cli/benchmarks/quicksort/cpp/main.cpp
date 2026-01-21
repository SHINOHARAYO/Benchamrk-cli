#include <iostream>
#include <vector>
#include <cstdlib>
#include <algorithm>
#include <random>

using namespace std;

int main(int argc, char* argv[]) {
    int n = 1000000;
    if (argc > 1) n = atoi(argv[1]);

    vector<int> data(n);
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis(0, 1000000);

    for(int i=0; i<n; ++i) data[i] = dis(gen);

    sort(data.begin(), data.end());

    cout << data[0] << endl;
    return 0;
}

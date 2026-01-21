#include <iostream>
#include <vector>
#include <cstdlib>
#include <random>

using namespace std;

vector<vector<double>> generate_matrix(int n) {
    vector<vector<double>> m(n, vector<double>(n));
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> dis(0.0, 1.0);
    for(int i=0; i<n; ++i)
        for(int j=0; j<n; ++j)
            m[i][j] = dis(gen);
    return m;
}

vector<vector<double>> mat_mul(const vector<vector<double>>& A, const vector<vector<double>>& B, int n) {
    vector<vector<double>> C(n, vector<double>(n, 0.0));
    for (int i = 0; i < n; ++i) {
        for (int k = 0; k < n; ++k) {
            for (int j = 0; j < n; ++j) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
    return C;
}

int main(int argc, char* argv[]) {
    int n = 200;
    if (argc > 1) n = atoi(argv[1]);

    auto A = generate_matrix(n);
    auto B = generate_matrix(n);
    auto C = mat_mul(A, B, n);
    
    cout << C[0][0] << endl;
    return 0;
}

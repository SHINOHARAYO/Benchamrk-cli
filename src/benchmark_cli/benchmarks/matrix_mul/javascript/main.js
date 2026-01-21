function generateMatrix(n) {
    const m = [];
    for (let i = 0; i < n; i++) {
        m[i] = [];
        for (let j = 0; j < n; j++) {
            m[i][j] = Math.random();
        }
    }
    return m;
}

function matMul(A, B, n) {
    const C = [];
    for (let i = 0; i < n; i++) {
        C[i] = new Float64Array(n);
        for (let k = 0; k < n; k++) {
            for (let j = 0; j < n; j++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
    return C;
}

const args = process.argv.slice(2);
const n = args.length > 0 ? parseInt(args[0]) : 200;

const A = generateMatrix(n);
const B = generateMatrix(n);
const C = matMul(A, B, n);
console.log(C[0][0]);

const http = require('http');

const PORT = 0; // Random port

function runServer(callback) {
    const server = http.createServer((req, res) => {
        res.writeHead(200, { 'Content-Type': 'text/plain', 'Content-Length': 11 });
        res.end('Hello World');
    });

    server.listen(PORT, () => {
        const port = server.address().port;
        callback(server, port);
    });
}

function runClient(port, n, callback) {
    let completed = 0;

    // Simple concurrent client loop? Or sequential?
    // Sequential to mimic Python loop for fair comparison?
    // Python code was sequential: conn.request -> getresponse -> read.
    // So we should chain requests.

    function makeRequest() {
        if (completed >= n) {
            callback();
            return;
        }

        const options = {
            hostname: '127.0.0.1',
            port: port,
            path: '/',
            method: 'GET',
            agent: new http.Agent({ keepAlive: true }) // Uses keep-alive
        };

        const req = http.request(options, (res) => {
            res.on('data', () => { }); // Consume
            res.on('end', () => {
                completed++;
                makeRequest(); // Next
            });
        });

        req.on('error', (e) => {
            console.error(e);
        });

        req.end();
    }

    makeRequest();
}

function main() {
    let n = 5000;
    if (process.argv.length > 2) {
        n = parseInt(process.argv[2]);
    }

    runServer((server, port) => {
        const start = process.hrtime();

        runClient(port, n, () => {
            const diff = process.hrtime(start);
            const duration = (diff[0] * 1e9 + diff[1]) / 1e9;
            // console.log(`Requests: ${n}, Time: ${duration.toFixed(4)}s`);
            server.close();
        });
    });
}

main();

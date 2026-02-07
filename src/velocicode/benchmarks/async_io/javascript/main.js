const { performance } = require('perf_hooks');

async function ioTask(duration) {
    return new Promise(resolve => {
        setTimeout(resolve, duration);
    });
}

async function main() {
    let n = 10000;
    if (process.argv.length > 2) {
        n = parseInt(process.argv[2]);
    }

    const duration = 10; // 10ms

    const start = performance.now();
    const tasks = [];
    for (let i = 0; i < n; i++) {
        tasks.push(ioTask(duration));
    }

    await Promise.all(tasks);
    const end = performance.now();

    // Output time in seconds? Velocicode typically handles timing via wrapper.
    // So main just runs.
}

main();

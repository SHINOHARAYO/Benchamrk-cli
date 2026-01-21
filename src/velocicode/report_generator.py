import json
import datetime

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Velocicode Benchmark Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f4f6f8; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .meta {{ color: #7f8c8d; font-size: 0.9em; margin-bottom: 30px; }}
        .benchmark-section {{ margin-bottom: 50px; }}
        .chart-container {{ position: relative; height: 300px; width: 100%; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #eee; }}
        th {{ background-color: #f8f9fa; }}
        .rank-1 {{ color: #f1c40f; font-weight: bold; }} /* Gold */
        .rank-2 {{ color: #95a5a6; font-weight: bold; }} /* Silver */
        .rank-3 {{ color: #cd7f32; font-weight: bold; }} /* Bronze */
    </style>
</head>
<body>
    <div class="container">
        <h1>Velocicode Report</h1>
        <div class="meta">Generated on: {date}</div>
        
        <div id="charts"></div>
    </div>

    <script>
        const results = {results_json};

        // Group results by benchmark
        const grouped = {{}};
        results.forEach(r => {{
            if (!grouped[r.benchmark]) grouped[r.benchmark] = [];
            grouped[r.benchmark].push(r);
        }});

        const container = document.getElementById('charts');

        // Color palette for languages
        const colors = {{
            'python': '#3572A5',
            'cpp': '#f34b7d',
            'rust': '#dea584',
            'go': '#00ADD8',
            'javascript': '#f1e05a'
        }};

        for (const [benchName, items] of Object.entries(grouped)) {{
            // Sort by mean time
            items.sort((a, b) => a.mean - b.mean);
            
            // Create Section
            const section = document.createElement('div');
            section.className = 'benchmark-section';
            
            const title = document.createElement('h2');
            title.textContent = `Benchmark: ${{benchName}}`;
            section.appendChild(title);
            
            // Canvas for Chart
            const chartDiv = document.createElement('div');
            chartDiv.className = 'chart-container';
            const canvas = document.createElement('canvas');
            chartDiv.appendChild(canvas);
            section.appendChild(chartDiv);
            
            // Table
            const table = document.createElement('table');
            table.innerHTML = `
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Language</th>
                        <th>Time (s)</th>
                        <th>Relative Speed</th>
                    </tr>
                </thead>
                <tbody>
                    ${{items.map((item, index) => {{
                        const relative = (item.mean / items[0].mean).toFixed(2) + 'x';
                        let rankClass = '';
                        let rankIcon = index + 1;
                        if (index === 0) {{ rankIcon = '🥇'; rankClass='rank-1'; }}
                        if (index === 1) {{ rankIcon = '🥈'; rankClass='rank-2'; }}
                        if (index === 2) {{ rankIcon = '🥉'; rankClass='rank-3'; }}
                        
                        return `<tr>
                            <td class="${{rankClass}}">${{rankIcon}}</td>
                            <td>${{item.language}}</td>
                            <td>${{item.mean.toFixed(4)}}</td>
                            <td>${{relative}}</td>
                        </tr>`;
                    }}).join('')}}
                </tbody>
            `;
            section.appendChild(table);
            
            container.appendChild(section);
            
            // Render Chart
            new Chart(canvas, {{
                type: 'bar',
                data: {{
                    labels: items.map(i => i.language),
                    datasets: [{{
                        label: 'Execution Time (seconds) - Lower is Better',
                        data: items.map(i => i.mean),
                        backgroundColor: items.map(i => colors[i.language] || '#cccccc'),
                        borderColor: '#222',
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    indexAxis: 'y',
                    scales: {{
                        x: {{ beginAtZero: true, title: {{ display: true, text: 'Seconds' }} }}
                    }}
                }}
            }});
        }}
    </script>
</body>
</html>
"""

def generate_html_report(results, output_path):
    report_html = HTML_TEMPLATE.format(
        date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        results_json=json.dumps(results)
    )
    
    with open(output_path, 'w') as f:
        f.write(report_html)

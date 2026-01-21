from velocicode.reporter import print_table

def test_print_table_empty(capsys):
    print_table([])
    captured = capsys.readouterr()
    assert "No results to display" in captured.out

def test_print_table_data(capsys):
    data = [{
        'benchmark': 'test_bench',
        'language': 'python',
        'mean': 1.23456,
        'min': 1.0,
        'max': 1.5
    }]
    print_table(data)
    captured = capsys.readouterr()
    assert "test_bench" in captured.out
    assert "python" in captured.out
    assert "1.2346" in captured.out # rounded

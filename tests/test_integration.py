import os
from velocicode.main import discover_benchmarks, load_config, check_dependencies

def test_discover_benchmarks():
    algos = discover_benchmarks()
    assert 'fibonacci' in algos
    assert 'matrix_mul' in algos
    assert 'quicksort' in algos
    assert 'primes' in algos

def test_load_config():
    config = load_config()
    assert 'languages' in config
    assert 'python' in config['languages']
    assert 'cpp' in config['languages']

def test_check_dependencies_runs(capsys):
    # This just tests that it runs without error and prints something
    config = load_config()
    check_dependencies(config)
    captured = capsys.readouterr()
    assert "Checking System Dependencies" in captured.out

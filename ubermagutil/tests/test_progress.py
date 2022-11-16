import time

import ubermagutil as uu


def test_bar(capsys, tmp_path):
    total = 10
    with uu.progress.bar(
        total=total,
        package_name="my package",
        runner_name="my runner",
        glob_name=f"{str(tmp_path)}/*.out",
    ):
        for i in range(total):
            (tmp_path / f"{i}.out").touch()
            time.sleep(0.1)
    captured = capsys.readouterr()
    assert "Running my package" in captured.out  # summary line at the end
    assert "took" in captured.out  # summary line at the end
    assert "files written" in captured.err  # tqdm writes to stderr


def test_summary(capsys):
    with uu.progress.summary("my package", "my runner"):
        pass
    captured = capsys.readouterr()
    assert "Running my package" in captured.out
    assert captured.err == ""


def test_quiet(capsys):
    with uu.progress.quiet():
        pass
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""

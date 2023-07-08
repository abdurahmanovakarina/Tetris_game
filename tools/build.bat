python ../setup.py bdist_wheel
python ../setup.py sdist
rd /s /q tetris_app.egg-info
rd /s /q build
move dist ..

# Things to be done

  - Reimplement generate.py from `geometer_scripts` to use [click](http://click.pocoo.org/6/)
  - Rename generate.py to geometer.py
  - Establish it as an entry point in the setup.py
  - Establish `install_requires` in setup.py for:
    - [click](http://click.pocoo.org/6/)
    - [PyObjC](http://pyobjc.readthedocs.io/en/latest/) if installed on macOS
    - [cairocffi](https://cairocffi.readthedocs.io/en/latest/) if cairo is already installed
    - [pillow](https://pillow.readthedocs.io/en/5.1.x/)
    - [pyx](http://pyx.sourceforge.net/documentation.html)

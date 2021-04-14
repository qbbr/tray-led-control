# tray-led-control

Tray App for control LED strip WS2812B over Arduino serial port

## depends

 * [python3](https://www.python.org/)
 * [wxPython](https://wxpython.org/)
 * [pySerial](https://github.com/pyserial/pyserial)

see [requirements.txt](requirements.txt) for more datail

## arduino sketch

[arduino-led-control](https://github.com/qbbr/arduino-led-control)

## run

```bash
./tray-led-control.py
# see help for more detail
./tray-led-control.py -h
```

![qbbr-arduino-tray-led-control](https://i.imgur.com/H0MsBGw.gif)

## dev

 * [python3-venv](https://docs.python.org/3/library/venv.html)

```bash
python3 -m venv venv
 . venv/bin/activate
pip install -r requirements.txt
```

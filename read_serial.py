import time
import serial
import argparse
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk


parser = argparse.ArgumentParser()

# Arguments for Serial
parser.add_argument("--baudrate", type=int, default=9600,
                    help="the baud rate of the serial port. do not specify for USB")

parser.add_argument("--bytesize", type=int, default=8,
                    help="the number of bits in a byte",
                    choices=[5, 6, 7, 8])

parser.add_argument("--parity", type=str, default="N",
                    help="parity checking on the serial port",
                    choices=["N", "E", "O", "M", "S"])

parser.add_argument("port", type=str, help="the serial port to read from")

parser.add_argument("--stopbits", type=str, default="1",
                    help="the number of stop bits",
                    choices=["1", "1.5", "2"])

parser.add_argument("--timeout", type=float, default=None,
                    help="read timeout value in seconds. None will wait forever "
                    "and 0 will enter non-blocking mode")

parser.add_argument("--xonxoff", type=bool, default=False,
                    help="enable or disable software flow control. should not "
                    "be enabled with rtscts")

parser.add_argument("--rtscts", type=bool, default=False,
                    help="enable or disable hardware flow control (RTS/CTS). "
                    "should not be enabled with xonxoff")

parser.add_argument("--dsrdts", type=bool, default=False,
                    help="enable or disable hardware flow control (DSR/DTR). "
                    "ignored on some platforms. False follows rtscts. should not "
                    "be enabled with xonxoff")


# Program arguments
parser.add_argument("--output", type=str, default="stdout",
                    help="where to send the data read from the serial port. "
                    "can be stdout or a valid file path",
                    choices=["stdout", "file_path"])

parser.add_argument("--rate", type=int, default=1,
                    help="rate at which to send data read from the serial port to the desired destination")

args = parser.parse_args()

baudrate = args.baudrate
bytesize = args.bytesize
port = args.port
timeout = args.timeout
xonxoff = args.xonxoff
rtscts = args.rtscts
dsrdtr = args.dsrdts


parity = args.parity
if args.parity == "N":
    parity = serial.PARITY_NONE
elif args.parity == "E":
    parity = serial.PARITY_EVEN
elif args.parity == "O":
    parity = serial.PARITY_ODD
elif args.parity == "M":
    parity = serial.PARITY_MARK
elif args.parity == "S":
    parity = serial.PARITY_SPACE

stopbits = args.stopbits
if stopbits == "1":
    stopbits = serial.STOPBITS_ONE
elif stopbits == "1.5":
    stopbits = serial.STOPBITS_ONE_POINT_FIVE
elif stopbits == "2":
    stopbits = serial.STOPBITS_TWO

output = args.output
rate_hz = args.rate
rate_s = 1.0 / rate_hz

ser = serial.Serial(port=args.port,
                    baudrate=baudrate,
                    bytesize=bytesize,
                    parity=parity,
                    stopbits=stopbits,
                    timeout=timeout,
                    xonxoff=xonxoff,
                    rtscts=rtscts,
                    dsrdtr=dsrdtr)

# GUI globals
builder = Gtk.Builder()
builder.add_from_file("./read_serial_gui4.glade")

button_action = builder.get_object("button_action")
win_top_level = builder.get_object("win_top_level")


def start_serial_monitor():
    return


def stop_serial_monitor():
    return


def control_serial_monitor(widget):
    classes = button_action.get_css_classes()

    if "button_start" in classes:
        button_action.remove_css_class("button_start")
        button_action.add_css_class("button_stop")
        button_action.set_label("stop")
        start_serial_monitor()

    else:
        button_action.remove_css_class("button_stop")
        button_action.add_css_class("button_start")
        button_action.set_label("start")
        stop_serial_monitor()


def gui_init(app):
    # screen = Gdk.Screen.get_default()
    provider = Gtk.CssProvider()
    provider.load_from_path("./read_serial_gui.css")
    Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(),
                                              provider,
                                              Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    button_action.connect('clicked', control_serial_monitor)

    # win_top_level.css.load_from_file("./read_serial_gui.css")
    win_top_level.set_application(app)
    win_top_level.present()


app = Gtk.Application(application_id='com.alexeast.ReadSerial')
app.connect('activate', gui_init)
app.run(None)

# while True:
#     t_start = time.time()
#     if ser.in_waiting > 0:
#         print(ser.readline())

#     wait = rate_s - time.time() - t_start
#     if wait > 0:
#         time.sleep(wait)
#     else:
#         time.sleep(rate_s)

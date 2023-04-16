import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, GObject
import serial
import threading
import time

ser = serial.Serial()
buffer = Gtk.TextBuffer()
rate_s = 1

# "--baudrate"
# type=int
# default=9600
# help="the baud rate of the serial port. do not specify for USB"

# "--bytesize"
# type=int
# default=8
# help="the number of bits in a byte"

# "--parity"
# type=str
# default="N"
# help="parity checking on the serial port"

# "port"
# type=str
# help="the serial port to read from"

# "--stopbits"
# type=str
# default="1"
# help="the number of stop bits"

# "--timeout"
# type=float
# default=None
# help="read timeout value in seconds. None will wait forever and 0 will enter non-blocking mode"

# "--xonxoff
# type=bool
# default=False
# help="enable or disable software flow control. should not be enabled with rtscts"

# "--rtscts
# type=bool
# default=False
# help="enable or disable hardware flow control (RTS/CTS). should not be enabled with xonxoff"

# "--dsrdts
# type=bool
# default=False
# help="enable or disable hardware flow control (DSR/DTR). ignored on some platforms. False follows rtscts. should not be enabled with xonxoff"

# "--rate"
# type=int
# default=1
# help="rate at which to send data read from the serial port to the desired destination"

class WorkerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        t_start = time.time()
        if ser.in_waiting > 0:
            buffer += ser.readline()
        leftover = rate_s - time.time() - t_start
        if leftover < 0:
            time.sleep(rate_s)
        else:
            time.sleep(leftover)

# GUI globals
builder = Gtk.Builder()
builder.add_from_file("./read_serial_gui4.glade")

button_action = builder.get_object("button_action")
check_dsrdts = builder.get_object("check_dsrdts")
check_rtscts = builder.get_object("check_rtscts")
combo_byte_size = builder.get_object("combo_byte_size")
combo_parity = builder.get_object("combo_parity")
combo_stop_bits = builder.get_object("combo_stop_bits")
check_xonxoff = builder.get_object("check_xonxoff")
entry_baud_rate = builder.get_object("entry_baud_rate")
entry_port = builder.get_object("entry_port")
entry_print_rate = builder.get_object("entry_print_rate")
entry_timeout = builder.get_object("entry_timeout")
text_view_received = builder.get_object("text_view_received")
win_top_level = builder.get_object("win_top_level")

def start_serial_monitor():
    try:
        ser.baudrate = int(entry_baud_rate.get_text())
    except:
        ser.baudrate = int(entry_baud_rate.get_placeholder_text())

    try:
        ser.bytesize = int(combo_byte_size.get_active_text())
    except:
        ser.bytesize = 8

    try:
        ser.timeout = float(entry_timeout.get_text())
    except:
        ser.timeout = float(entry_timeout.get_placeholder_text())

    try:
        ser.xonxoff = bool(check_xonxoff.get_active())
    except:
        ser.xonxoff = False

    try:
        ser.rtscts = bool(check_rtscts.get_active())
    except:
        ser.rtscts = False

    try:
        ser.dsrdtr = bool(check_dsrdts.get_active())
    except:
        ser.dsrdtr = False

    selected = combo_parity.get_active_text()
    if selected == "" or selected == "None":
        ser.parity = serial.PARITY_NONE
    elif selected == "Even":
        ser.parity = serial.PARITY_EVEN
    elif selected == "Odd":
        ser.parity = serial.PARITY_ODD
    elif selected == "Mark":
        ser.parity = serial.PARITY_MARK
    elif selected == "Space":
        ser.parity = serial.PARITY_SPACE

    selected = combo_stop_bits.get_active_text()
    if selected == "" or selected == "1":
        ser.stopbits = serial.STOPBITS_ONE
    elif selected == "1.5":
        ser.stopbits = serial.STOPBITS_ONE_POINT_FIVE
    elif selected == "2":
        ser.stopbits = serial.STOPBITS_TWO

    if entry_port.get_text() == "":
        ser.port = entry_port.get_placeholder_text()
    else:
        ser.port = entry_port.get_text()

    try:
        rate_s = 1.0 / float(entry_print_rate.get_text())
    except:
        rate_s = 1.0 / float(entry_print_rate.get_placeholder_text())

    ser.open()
    return


def stop_serial_monitor():
    ser.close()
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
    provider = Gtk.CssProvider()
    provider.load_from_path("./read_serial_gui.css")
    Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(),
                                              provider,
                                              Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    button_action.connect('clicked', control_serial_monitor)

    combo_byte_size.set_active(0)
    combo_parity.set_active(0)
    combo_stop_bits.set_active(0)

    text_view_received.set_overwrite(False)

    win_top_level.set_application(app)
    win_top_level.present()


app = Gtk.Application(application_id='com.alexeast.ReadSerial')
app.connect('activate', gui_init)
app.run(None)
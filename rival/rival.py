import yaml
import pyudev
import hidrawpure as hidraw
import webcolors

RIVAL_HID_ID = '0003:00001038:00001384'

LED_LOGO = 1
LED_WHEEL = 2

LED_STYLE_STEADY = 1
LED_STYLE_BREATHE_SLOW = 2
LED_STYLE_BREATHE_MEDIUM = 3
LED_STYLE_BREATHE_FAST = 4


def find_device_path():
    """find the appropriate /dev/hidrawX device to control the mouse"""
    ctx = pyudev.Context()
    for dev in ctx.list_devices(HID_ID=RIVAL_HID_ID):
        if dev.sequence_number == 0:
            children = list(dev.children)
            if children:
                child = children[0]
                if child.subsystem == 'hidraw':
                    return child['DEVNAME']


def open_device(dev_path=None):
    if dev_path is None:
        dev_path = find_device_path()
    return hidraw.HIDRaw(open(dev_path, 'w+'))


def send(report, device=None):
    """send a report packet to the device"""
    if device is None:
        device = open_device()
    device.sendFeatureReport(report)

def set_led_color(led, color):
    if led not in (LED_LOGO, LED_WHEEL):
        raise ValueError("Invalid LED: %s" % (led,))
    if isinstance(color, basestring):
        try:
            color = webcolors.name_to_rgb(color)
        except ValueError:
            try:
                color = webcolors.hex_to_rgb(color)
            except ValueError:
                color = webcolors.hex_to_rgb("#" + color)

    if not hasattr(color, '__iter__'):
        raise ValueError("Invalid Color: %s" % (color, ))

    args = (chr(led),) + tuple([chr(b) for b in color])
    return "\x08%s%s%s%s" % args

def set_led_style(led, style):
    if led not in (LED_LOGO, LED_WHEEL):
        raise ValueError("Invalid LED: %s" % (led,))
    if 1 <= style <= 4:
        return '\x07%s%s' % (chr(led), chr(style))
    raise ValueError("Invalid Style %s, valid values are 1, 2, 3 and 4" % (style,))

def set_wheel_color(color):
    return set_led_color(LED_WHEEL, color)

def set_logo_color(color):
    return set_led_color(LED_LOGO, color)

def set_wheel_style(style):
    return set_led_style(LED_WHEEL, style)

def set_logo_style(style):
    return set_led_style(LED_LOGO, style)

def set_cpi(cpinum, value):
    if cpinum not in (1,2):
        raise ValueError("Invalid CPI Number: %s" % (cpinum,))
    if value % 50:
        raise ValueError("CPI Must be increments of 50")
    if not (50 <= value <= 6500):
        raise ValueError("CPI Must be between 50 and 6500")
    return '\x03%s%s' % (chr(cpinum), chr(value/50),)

def set_cpi_1(value):
    return set_cpi(1, value)


def set_cpi_2(value):
    return set_cpi(2, value)

def commit():
    return '\x09'

def set_polling_rate(rate):
    if rate == 1000:
        b = '\x01'
    elif rate == 500:
        b = '\x02'
    elif rate == 250:
        b = '\x03'
    elif rate == 125:
        b = '\x04'
    else:
        raise ValueError("Invalid Polling Rate, valid values are 1000, 500, 250 and 125")
    return "\x04\x00%s" % (b,)


class Profile(object):

    def __init__(self):
        self._logo_color = (0, 0, 0)
        self._wheel_color = (0, 0, 0)
        self.logo_style = LED_STYLE_STEADY
        self.wheel_style = LED_STYLE_STEADY
        self.cpi1 = 800
        self.cpi2 = 1600
        self.polling_rate = 1000

    def _normalize_color(self, value):
        rgb = None
        try:
            if isinstance(value, basestring):
                if value.startswith("#"):
                    rgb = webcolors.hex_to_rgb(value)
                else:
                    rgb = webcolors.name_to_rgb(value)
            elif hasattr(value, '__iter__'):
                rgb = tuple(value)
        except ValueError as e:
            pass

        return rgb

    @property
    def logo_color(self):
        return self._logo_color

    @logo_color.setter
    def logo_color(self, value):
        rgb = self._normalize_color(value)
        if not rgb:
            raise ValueError("Invalid Color: %s" % (value,))
        self._logo_color = rgb

    @property
    def wheel_color(self):
        return self._wheel_color

    @wheel_color.setter
    def wheel_color(self, value):
        rgb = self._normalize_color(value)
        if not rgb:
            raise ValueError("Invalid Color: %s" % (value,))
        self._wheel_color = rgb

    @classmethod
    def copy_profile(cls, profile):
        newprofile = Profile()
        newprofile.logo_color = tuple(profile.logo_color)
        newprofile.wheel_color = tuple(profile.wheel_color)
        newprofile.logo_style = profile.logo_style
        newprofile.wheel_style = profile.wheel_style
        newprofile.cpi1 = profile.cpi1
        newprofile.cpi2 = profile.cpi2
        newprofile.polling_rate = profile.polling_rate
        return newprofile

    @classmethod
    def from_yaml(cls, stream):
        cfg = yaml.load(stream)
        profile = cls.copy_profile(FACTORY_PROFILE)
        print cfg, profile
        for k, v in cfg.items():
            if hasattr(profile, k):
                setattr(profile, k, v)
        return profile

    def to_report_list(self, current_state=None):
        items = [
            set_wheel_color(self.wheel_color),
            set_wheel_style(self.wheel_style),
            set_logo_color(self.logo_color),
            set_logo_style(self.logo_style),
            set_cpi_1(self.cpi1),
            set_cpi_2(self.cpi2),
            set_polling_rate(self.polling_rate)
        ]
        if current_state:
            return [i for i in items if i not in current_state]
        return items


FACTORY_PROFILE = Profile()
FACTORY_PROFILE.logo_color = (255, 24, 0)
FACTORY_PROFILE.wheel_color = (255, 24, 0)
FACTORY_PROFILE.logo_style = 2
FACTORY_PROFILE.wheel_style = 2
FACTORY_PROFILE.cpi1 = 800
FACTORY_PROFILE.cpi2 = 1600
FACTORY_PROFILE.polling_rate = 1000

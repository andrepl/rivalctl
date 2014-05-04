import unittest
from rival import *

class TestBasicSets(unittest.TestCase):

    def test_set_led_color(self):
        self.assertEqual(set_led_color(LED_WHEEL, 'white'), '\x08\x02\xFF\xFF\xFF')
        self.assertEqual(set_led_color(LED_LOGO, 'white'), '\x08\x01\xFF\xFF\xFF')

        self.assertEqual(set_led_color(LED_WHEEL, 'fff'), '\x08\x02\xFF\xFF\xFF')
        self.assertEqual(set_led_color(LED_LOGO, 'fff'), '\x08\x01\xFF\xFF\xFF')

        self.assertEqual(set_led_color(LED_WHEEL, 'ffffff'), '\x08\x02\xFF\xFF\xFF')
        self.assertEqual(set_led_color(LED_LOGO, 'ffffff'), '\x08\x01\xFF\xFF\xFF')

        self.assertEqual(set_led_color(LED_WHEEL, '#ffffff'), '\x08\x02\xFF\xFF\xFF')
        self.assertEqual(set_led_color(LED_LOGO, '#ffffff'), '\x08\x01\xFF\xFF\xFF')

        self.assertEqual(set_wheel_color('black'), set_led_color(LED_WHEEL, 'black'))
        self.assertEqual(set_logo_color('black'), set_led_color(LED_LOGO, 'black'))

        self.assertRaises(ValueError, set_led_color, LED_WHEEL, 0)
        self.assertRaises(ValueError, set_led_color, LED_WHEEL, "poop-brown")
        self.assertRaises(ValueError, set_led_color, LED_WHEEL, "#hexy")
        self.assertRaises(ValueError, set_led_color, LED_WHEEL, None)
        self.assertRaises(ValueError, set_led_color, 0, "#FFF")

        self.assertRaises(ValueError, set_wheel_color, 0)
        self.assertRaises(ValueError, set_logo_color, 0)



    def test_set_led_style(self):
        self.assertEqual(set_led_style(LED_LOGO, LED_STYLE_STEADY), '\x07\x01\x01')
        self.assertEqual(set_led_style(LED_LOGO, LED_STYLE_BREATHE_SLOW), '\x07\x01\x02')
        self.assertEqual(set_led_style(LED_LOGO, LED_STYLE_BREATHE_MEDIUM), '\x07\x01\x03')
        self.assertEqual(set_led_style(LED_LOGO, LED_STYLE_BREATHE_FAST), '\x07\x01\x04')
        self.assertEqual(set_led_style(LED_WHEEL, LED_STYLE_STEADY), '\x07\x02\x01')
        self.assertEqual(set_led_style(LED_WHEEL, LED_STYLE_BREATHE_SLOW), '\x07\x02\x02')
        self.assertEqual(set_led_style(LED_WHEEL, LED_STYLE_BREATHE_MEDIUM), '\x07\x02\x03')
        self.assertEqual(set_led_style(LED_WHEEL, LED_STYLE_BREATHE_FAST), '\x07\x02\x04')

        self.assertEqual(set_wheel_style(LED_STYLE_STEADY), set_led_style(LED_WHEEL, LED_STYLE_STEADY))
        self.assertEqual(set_logo_style(LED_STYLE_STEADY), set_led_style(LED_LOGO, LED_STYLE_STEADY))

        self.assertRaises(ValueError, set_led_style, LED_WHEEL, 0)
        self.assertRaises(ValueError, set_led_style, LED_WHEEL, 5)
        self.assertRaises(ValueError, set_led_style, 0, LED_STYLE_BREATHE_MEDIUM)
        self.assertRaises(ValueError, set_led_style, 3, LED_STYLE_BREATHE_MEDIUM)

        self.assertRaises(ValueError, set_wheel_style, 0)
        self.assertRaises(ValueError, set_logo_style, 0)

    def test_set_cpi(self):
        self.assertEqual(set_cpi(1, 50), '\x03\x01\x01')
        self.assertEqual(set_cpi(2, 50), '\x03\x02\x01')
        self.assertEqual(set_cpi(1, 800), '\x03\x01\x10')
        self.assertEqual(set_cpi(2, 1600), '\x03\x02\x20')
        self.assertEqual(set_cpi(1, 6500), '\x03\x01\x82')
        self.assertEqual(set_cpi(2, 6500), '\x03\x02\x82')

        self.assertEqual(set_cpi_1(50), set_cpi(1, 50))
        self.assertEqual(set_cpi_2(50), set_cpi(2, 50))

        self.assertRaises(ValueError, set_cpi, 0, 100)
        self.assertRaises(ValueError, set_cpi, 3, 100)
        self.assertRaises(ValueError, set_cpi, 1, 0)
        self.assertRaises(ValueError, set_cpi, 1, 25)
        self.assertRaises(ValueError, set_cpi, 1, 55)
        self.assertRaises(ValueError, set_cpi, 1, 7500)
        self.assertRaises(ValueError, set_cpi_1, 55)
        self.assertRaises(ValueError, set_cpi_2, 7500)

    def test_set_polling_rate(self):
        self.assertEqual(set_polling_rate(125), '\x04\x00\x04')
        self.assertEqual(set_polling_rate(250), '\x04\x00\x03')
        self.assertEqual(set_polling_rate(500), '\x04\x00\x02')
        self.assertEqual(set_polling_rate(1000), '\x04\x00\x01')
        self.assertRaises(ValueError, set_polling_rate, 900)
        self.assertRaises(ValueError, set_polling_rate, 0)
        self.assertRaises(ValueError, set_polling_rate, -100)

    def test_commit(self):
        self.assertEqual(commit(), '\x09')


class TestProfile(unittest.TestCase):
    def test_default_report_list(self):
        profile = Profile()
        reportlist = profile.to_report_list()
        self.assertIn('\x08\x01\x00\x00\x00', reportlist)
        self.assertIn('\x08\x02\x00\x00\x00', reportlist)
        self.assertIn('\x07\x01\x01', reportlist)
        self.assertIn('\x07\x02\x01', reportlist)
        self.assertIn('\x04\x00\x01', reportlist)
        self.assertIn('\x03\x01\x10', reportlist)
        self.assertIn('\x03\x02\x20', reportlist)
        self.assertEqual(len(reportlist), 7)

    def test_color_setters(self):
        profile = Profile()
        profile.logo_color = 'white'
        self.assertEqual(profile.logo_color, (255,255,255))

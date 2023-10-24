from escpos.printer import Usb

printer = Usb(0x0416, 0x5011)
#printer.image("assets/cartel.jpg")
printer.text("¿Hola como estas?\n")
printer.close()

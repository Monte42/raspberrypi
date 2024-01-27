from pyPS4Controller.controller import Controller

class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_x_press(self):
        print("Hello world")

    def on_x_release(self):
        print("Goodbye world")

    def on_L3_up(self, value):
        dividend = 32767 / 100
        print(round(value/dividend))
    def on_L3_y_at_rest(self):
        print('stop')

    def on_L3_down(self, value):
        dividend = 32767 / 100
        print(round(value/dividend))

    def on_triangle_release(self):
        pass
        # print(f) # < -- this breaks the controller class, exit plan


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()
import dearpygui.dearpygui as dpg
import dpg_util as dpg_util
from gui import Gui


@dpg_util.setup
def main() -> None:
    Gui().run()
    dpg.set_primary_window(window="main_window", value=True)
    # dpg.maximize_viewport()


if __name__ == "__main__":
    w = 700
    x = 900 - w // 2
    viewport_config = {
        "title": "e-menu",
        "width": w,
        "height": 600,
        "x_pos": x,
        "y_pos": 0,
    }
    main(**viewport_config)

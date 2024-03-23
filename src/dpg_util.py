import functools
from typing import Callable, Union, Any
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import dearpygui_ext.logger as logger


def logger_window(tag: Union[str, int]):
    with dpg.window(menubar=False, width=300, height=300, pos=(0, 0),
                    tag=tag, show=False) as w:
        return w, logger.mvLogger(parent=w)


def setup(fn):
    def wrap(**kwargs):
        dpg.create_context()
        dpg.create_viewport(**kwargs)
        dpg.setup_dearpygui()
        dpg.bind_theme(get_theme())
        fn()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    return wrap


def help_tooltip(message: str, icon_color=(149, 156, 161)) -> None:
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True)
    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))
    t = dpg.add_text("(?)", color=icon_color)
    with dpg.tooltip(t):
        dpg.add_text(message)


def add_tools():
    with dpg.menu(label="Tools"):
        # dpg.add_menu_item(label="dpg Demo", callback=lambda: demo.show_demo())
        # dpg.add_menu_item(label="imgui Demo", callback=lambda: dpg.show_imgui_demo())
        # dpg.add_menu_item(label="implot Demo", callback=lambda: dpg.show_implot_demo())
        dpg.add_menu_item(label="Show About", callback=lambda: dpg.show_tool(dpg.mvTool_About))
        # dpg.add_menu_item(label="Save Ini File", callback=lambda: dpg.save_init_file("custom_layout.ini"))
        dpg.add_menu_item(label="Show Metrics", callback=lambda: dpg.show_tool(dpg.mvTool_Metrics))
        dpg.add_menu_item(label="Show Documentation", callback=lambda: dpg.show_tool(dpg.mvTool_Doc), )
        dpg.add_menu_item(label="Show Debug", callback=lambda: dpg.show_tool(dpg.mvTool_Debug))
        dpg.add_menu_item(label="Show Style Editor", callback=lambda: dpg.show_tool(dpg.mvTool_Style), )
        dpg.add_menu_item(label="Show Font Manager", callback=lambda: dpg.show_tool(dpg.mvTool_Font), )
        dpg.add_menu_item(label="Show Item Registry", callback=lambda: dpg.show_tool(dpg.mvTool_ItemRegistry), )


def get_theme():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 2, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 4, 4, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 10, 10, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.5, 0.5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 7, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 4, category=dpg.mvThemeCat_Core)

            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (128, 128, 128, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (15, 15, 15, 240), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255, 255, 255, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (20, 20, 20, 240), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (110, 110, 128, 128), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (51, 54, 56, 138), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (102, 102, 102, 102), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (46, 46, 46, 171), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (10, 10, 10, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (74, 74, 74, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (0, 0, 0, 130), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (36, 36, 36, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (5, 5, 5, 135), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (79, 79, 79, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (105, 105, 105, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (130, 130, 130, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (240, 240, 240, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (130, 130, 130, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (219, 219, 219, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Button, (112, 112, 112, 102), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (117, 120, 122, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (107, 107, 107, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Header, (179, 179, 179, 79), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (179, 179, 179, 204), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (122, 128, 133, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Separator, (110, 110, 128, 128), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorHovered, (184, 184, 184, 199), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorActive, (130, 130, 130, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGrip, (232, 232, 232, 64), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripHovered, (207, 207, 207, 171), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripActive, (117, 117, 117, 242), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Tab, (46, 89, 148, 220), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (66, 150, 250, 204), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, (51, 105, 173, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused, (17, 26, 38, 248), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive, (35, 67, 108, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_DockingPreview, (66, 150, 250, 179), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_DockingEmptyBg, (51, 51, 51, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_PlotLines, (156, 156, 156, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_PlotLinesHovered, (255, 110, 89, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, (186, 153, 38, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogramHovered, (255, 153, 0, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, (222, 222, 222, 89), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_DragDropTarget, (255, 255, 0, 230), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_NavHighlight, (153, 153, 153, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingHighlight, (255, 255, 255, 179),
                                category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingDimBg, (204, 204, 204, 51), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg, (204, 204, 204, 89), category=dpg.mvThemeCat_Core)
    return global_theme

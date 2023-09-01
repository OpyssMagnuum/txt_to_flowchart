# -*- coding: cp1251 -*-
import os
import file_work as fw
import draw as draw
import PySimpleGUI as sg
from pathlib import Path

# ==========KPACUBO=========


def main_window():
    size_b = 17
    layout_main = [[sg.B('���������', s=12, key='Settings')],

                   [sg.T('����: ', s=size_b, justification="r"), sg.Input(settings['File']['path_file'],
                                                                          key="-IN-", enable_events=True),
                    sg.FileBrowse('�����', file_types=(("��������� �����", '*.txt'),))],

                   [sg.B('�����', key='Exit', expand_x=True, s=size_b, button_color='tomato'),
                    sg.B('����', key='FileB', expand_x=True, s=size_b),
                    sg.B('�����', key='Scheme', expand_x=True, s=size_b)]
                   ]

    window = sg.Window('�������������������', layout_main, size=(1000, 170))

    while True:
        event, values = window.read()
        #print(event, values)
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break
        if event == '-IN-':
            settings['File']['path_file'] = values['-IN-']
        if event == 'Scheme':
            window.disappear()
            draw.draw_graph(int(settings['Graph']['w']), int(settings['Graph']['h']),
                            fw.find_Main(fw.enter_scheme(False, settings["File"]["path_file"])),
                            fw.find_Extra(fw.enter_scheme(False, settings["File"]["path_file"]),
                                          settings["File"]["path_file"]),
                            int(settings['File']['char_limit']), settings["File"]["path_file"], settings)
            window.reappear()
        if event == 'FileB':
            os.startfile(settings['File']['path_file'])
        if event == 'Settings':
            Settings(settings)

    window.close()


def Settings(settings):
    layout = [[sg.T('�����', font=("Helvetica", 20, "bold"), background_color='#00A89D')],

              [sg.T('�����', justification='left'), sg.I(settings['Graph']['fontname'], s=12, key='fontname'),
               sg.T('������', justification='left'), sg.I(settings['Graph']['size'], s=4, key='size')],

              [sg.T('�������� ��������', font=("Helvetica", 20, "bold"), background_color='#00A89D')],
              [sg.T('�����', justification='left'),
               sg.Combo(['�������', '� �����'], '�������' if settings['Graph']['m_linestyle'] == 'solid'
               else '� �����', s=10, key='m_boxstyle'),
               sg.T('������ �����', justification='left'),
               sg.I(settings['Graph']['m_linewidth'], s=4, key='m_linewidth')],

              [sg.T('�������������� ��������', font=("Helvetica", 20, "bold"), background_color='#00A89D')],
              [sg.T('�����', justification='left'),
               sg.Combo(['�������', '� �����'], '�������' if settings['Graph']['ex_linestyle'] == 'solid'
               else '� �����', s=10, key='ex_boxstyle'),
               sg.T('������ �����', justification='left'),
               sg.I(settings['Graph']['ex_linewidth'], s=4, key='ex_linewidth')],

              [sg.T('������', font=("Helvetica", 20, "bold"), background_color='#00A89D')],
              [sg.T('��������� ���������� |', justification='left'), sg.T('x0'),
               sg.I(settings['Graph']['x_0'], s=6, key='x0'), sg.T('y0'), sg.I(settings['Graph']['y_0'], s=6, key='y0')],

              [sg.T('������ |', justification='left'), sg.T('������'),
               sg.I(settings['Graph']['w'], s=6, key='w'), sg.T('������'), sg.I(settings['Graph']['h'], s=6, key='h')],

              [sg.B('�����', key='Exit', button_color='tomato'),
               sg.B('������� �����������', key='Default'), sg.B('�����������', key='Advanced'),
               sg.B('���������', key='Save')]]

    window = sg.Window('���������', layout, modal=True)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break
        if event == "Save":
            settings['Graph']['fontname'] = values['fontname']
            settings['Graph']['size'] = values['size']
            settings['Graph']['m_linestyle'] = 'solid' if values['m_boxstyle'] == '�������' else 'dotted'
            settings['Graph']['ex_linestyle'] = 'solid' if values['ex_boxstyle'] == '�������' else 'dotted'
            settings['Graph']['m_linewidth'] = values['m_linewidth']
            settings['Graph']['ex_linewidth'] = values['ex_linewidth']
            settings['Graph']['x_0'] = values['x0']
            settings['Graph']['y_0'] = values['y0']
            settings['Graph']['w'] = values['w']
            settings['Graph']['h'] = values['h']
            sg.popup_no_titlebar("��������� ���������!")

        if event == 'Default':
            if sg.popup_yes_no('������� ����������� ���������?') == 'Yes':
                settings['Graph']['fontname'] = 'Helvetica'
                settings['Graph']['size'] = '10'
                settings['Graph']['m_linestyle'] = 'solid'
                settings['Graph']['ex_linestyle'] = 'dotted'
                settings['Graph']['m_linewidth'] = '2.0'
                settings['Graph']['ex_linewidth'] = '2.0'
                settings['Graph']['x_0'] = '0'
                settings['Graph']['y_0'] = '1000'
                settings['Graph']['w'] = '1200'
                settings['Graph']['h'] = '1500'

                settings['Graph']['coef_w'] = '1'
                settings['Graph']['coef_h'] = '2'
                settings['Graph']['distance'] = '40'
                settings['Graph']['multialignment'] = 'center'
                settings['File']['char_limit'] = '20'
                break
        if event == 'Advanced':
            advanced_settings(settings)

    window.close()


def advanced_settings(settings):
    layout = [[sg.T('������������'), sg.Combo(['center', 'left', 'right'],
                                              default_value=settings['Graph']['multialignment'], key='multi')],

              [sg.T('����������� ����'), sg.I(settings['File']['char_limit'], s=5, key='ch_lim')],

              [sg.T('����. h'), sg.I(settings['Graph']['coef_h'], s=5, key='coef_h')],

              [sg.T('����. w'), sg.I(settings['Graph']['coef_w'], s=5, key='coef_w')],

              [sg.T('���������'), sg.I(settings['Graph']['distance'], s=5, key='distance')],

              [sg.B('�����', key='Exit', button_color='tomato'), sg.B('���������', key='save')]]

    window = sg.Window('����������� ���������', layout, modal=True)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break
        if event == 'save':
            settings['Graph']['coef_w'] = values['coef_w']
            settings['Graph']['coef_h'] = values['coef_h']
            settings['Graph']['distance'] = values['distance']
            settings['Graph']['multialignment'] = values['multi']
            settings['File']['char_limit'] = values['ch_lim']
            sg.popup_no_titlebar("����������� ��������� ���������!")

    window.close()


if __name__ == "__main__":
    SETTINGS_PATH = Path.cwd()
    settings = sg.UserSettings(
        path=SETTINGS_PATH, filename="config.ini", use_config_file=True, convert_bools_and_none=True
    )
    font_size = 17
    font_family = 'Arial'
    sg.set_options(font=(font_family, font_size))
    main_window()

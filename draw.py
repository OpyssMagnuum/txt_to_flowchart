import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator
from matplotlib.ticker import LinearLocator
import file_work as fw

arrowprops = {
    'arrowstyle': '->',
}

coords = []
ex_coords = []
bobox = [0, 1]
main_widths = []
main_heights = []
ex_widths = []
ex_heights = []


def getAllMyEx(ex_str, ident):
    r_str = []
    for i in range(len(ex_str)):
        check = True
        for j in range(len(str(ident))):
            if str(ident)[j] == str(ex_str[i])[j] and ex_str[i][j].isdigit():
                pass
            else:
                check = False
                break
            if (j + 1) == len(str(ident)):
                if ex_str[i][j + 1].isdigit():
                    check = False
        if check:
            r_str.append(ex_str[i])
    return r_str


def draw_Main(cx_0, cy_0, ax, first, stroka, str_index, ch_limit, r, coef_w, coef_h, ex_stroka, settings, font):
    # ====1
    ex_coords.clear()
    ex_widths.clear()
    ex_heights.clear()
    if first:
        t_m = ax.text(cx_0, cy_0, fw.razdel(stroka[str_index], ch_limit),
                      bbox={"fill": False,
                            "linestyle": settings["Graph"]["m_linestyle"],
                            "linewidth": float(settings["Graph"]["m_linewidth"])},
                      **font)
        bb = t_m.get_window_extent(renderer=r)
        bobox[0] = bb.width
        bobox[1] = bb.height
        main_widths.append(bb.width)
        main_heights.append(bb.height)

        # рисуем доп элементы
        exlist = getAllMyEx(ex_stroka, str_index + 1)  # str_index - от 0
        if len(exlist) > 0:
            first = True
            for i in range(len(exlist)):
                draw_Ex(ax, exlist[i], r, coef_h, ch_limit, first, i, str_index, settings, font)
                first = False

            draw_lines_ex(ax=ax, coef_h=coef_h, coef_w=coef_w, xm=cx_0, ym=cy_0, wm=bb.width, settings=settings)
    # =====2
    else:
        coords.append(cx_0 + (bobox[0] / coef_w) + float(settings['Graph']['distance']))
        coords.append(cy_0)
        cx_1 = coords[len(coords) - 2]
        cy_1 = coords[len(coords) - 1]
        t_m = ax.text(cx_1, cy_1, fw.razdel(stroka[str_index], ch_limit),
                      bbox={"fill": False,
                            "linestyle": settings["Graph"]["m_linestyle"],
                            "linewidth": float(settings["Graph"]["m_linewidth"])},
                      **font)
        bb = t_m.get_window_extent(renderer=r)
        bobox[0] = bb.width
        bobox[1] = bb.height
        main_widths.append(bb.width)
        main_heights.append(bb.height)
        # доп элементы
        exlist = getAllMyEx(ex_stroka, str_index + 1)  # str_index - от 0
        if len(exlist) > 0:
            first = True
            for i in range(len(exlist)):
                draw_Ex(ax, exlist[i], r, coef_h, ch_limit, first, i, str_index, settings, font)
                first = False
            draw_lines_ex(ax=ax, coef_h=coef_h, coef_w=coef_w, xm=cx_1, ym=cy_1, wm=bb.width, settings=settings)


def draw_Ex(ax, stroka, r, coef_h, ch_limit, first, ident, str_id, settings, font):
    if first:
        ex_coords.append(coords[str_id * 2])  # x как ix,iy в drawgraph()
        ex_coords.append(coords[str_id * 2 + 1])  # y
        t_ex = ax.text(ex_coords[0], ex_coords[1], fw.razdel(stroka, ch_limit),
                       bbox={"fill": False,
                             "linestyle": settings["Graph"]["ex_linestyle"],
                             "linewidth": float(settings["Graph"]["ex_linewidth"])},
                       **font)
        bb_ex = t_ex.get_window_extent(renderer=r)
        ex_coords[1] -= (bb_ex.height + float(settings['Graph']['distance'])) * coef_h
        t_ex.set_position((ex_coords[0], ex_coords[1]))

    else:
        ex_coords.append(ex_coords[ident * 2 - 2])
        ex_coords.append(ex_coords[ident * 2 - 1])
        t_ex = ax.text(ex_coords[-2], ex_coords[-1], fw.razdel(stroka, int(settings['File']['char_limit'])),
                       # если что тут левые нижние границы рамки
                       bbox={"fill": False,
                             "linestyle": settings["Graph"]["ex_linestyle"],
                             "linewidth": float(settings["Graph"]["ex_linewidth"])},
                       **font)
        bb_ex = t_ex.get_window_extent(renderer=r)
        ex_coords[-1] -= (bb_ex.height + float(settings['Graph']['distance'])) * coef_h
        t_ex.set_position((ex_coords[-2], ex_coords[-1]))
    ex_widths.append(bb_ex.width)
    ex_heights.append(bb_ex.height)


def draw_lines_m(ax, coef_w, settings):
    height = (coords[1] + coords[1] + min(main_heights) * float(settings['Graph']['coef_h'])) / 2
    for i in range(0, len(coords) - 2, 2):
        ch1 = coords[i] + main_widths[0] / coef_w - float(settings['Graph']['distance']) / (coef_w * 3)
        ch2 = coords[i + 2] - (float(settings['Graph']['distance']) / 5) * coef_w
        ax.annotate('', xytext=[ch1, height], xy=[ch2, height], arrowprops=dict(arrowstyle="->", color='black'))


def draw_lines_ex(ax, coef_h, coef_w, xm, ym, wm, settings):
    # первый элемент
    x0 = (xm + xm + wm / coef_w) / 2
    ch1 = ym - (float(settings['Graph']['distance']) / 2) * coef_h
    ch2 = ex_coords[1] + ex_heights[0] * coef_h + float(settings['Graph']['distance']) / 2
    ax.plot([x0, x0], [ch1, ch2], ':', color='black')
    # все после 1го элемента
    for i in range(1, len(ex_coords) - 2, 2):
        ch1 = ex_coords[i] - (float(settings['Graph']['distance']) / 2) * coef_h
        ch2 = ex_coords[i + 2] + ex_heights[i // 2 + 1] * coef_h + float(settings['Graph']['distance']) / 2
        ax.plot([x0, x0], [ch1, ch2], ':', color='black')


def turn_off_axis(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)


def control_axis(check, loc, ax):
    if loc != 0:
        ax.xaxis.set_major_locator(LinearLocator(loc))  # {
        ax.yaxis.set_major_locator(LinearLocator(loc))  # {
    if check:
        ax.grid()
    else:
        ax.xaxis.set_major_locator(NullLocator())
        ax.yaxis.set_major_locator(NullLocator())
        turn_off_axis(ax)


def draw_graph(width, height, stroka, ex_stroka, char_limit, read_from, settings):
    coords[:] = []
    main_widths[:] = []
    main_heights[:] = []
    coords.append(int(settings['Graph']['x_0']))
    coords.append(int(settings['Graph']['y_0']))

    fig = plt.figure()

    ax = fig.add_subplot()

    x0 = 0
    y0 = 0
    ax.set(ylim=[y0, height], xlim=[x0, width])  # размеры
    r = fig.canvas.get_renderer()

    font = {
        'size': settings["Graph"]["size"],
        'multialignment': settings["Graph"]["multialignment"]}

    # -~ drawing ~-
    first = True
    for i in range(len(fw.find_Main(fw.enter_scheme(False, read_from)))):
        if first:
            ix = 0
            iy = 1
        else:
            ix = i * 2 - 2
            iy = i * 2 - 1
        draw_Main(cx_0=coords[ix], cy_0=coords[iy], ax=ax, first=first, stroka=stroka, str_index=i, ch_limit=char_limit,
                  r=r, coef_w=float(settings['Graph']['coef_w']), coef_h=float(settings['Graph']['coef_h']),
                  ex_stroka=ex_stroka, settings=settings, font=font)
        first = False

    draw_lines_m(ax, float(settings['Graph']['coef_w']), settings)
    control_axis(False, 0, ax)
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')
    plt.show()

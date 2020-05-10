import matplotlib as mpl


SizeTitlePaper = 20
SizeLabelPaper = 18
SizeTickPaper = 16
SizeTitleSlides = 28
SizeLabelSlides = 24
SizeTickSlides = 20


def set_style():
    """
    Set styling for plots
    """
    mpl.pyplot.style.use('seaborn-paper')
    set_figsize()
    set_font()


def set_figsize():
    """
    Set default figsize
    """
    mpl.rcParams['figure.figsize'] = (12, 8)


def set_font(output='slides'):
    """
    Set font style

    Parameters
    ----------
    output: 'slides' or 'paper'
    """
    if output == 'slides':
        size_label = SizeLabelSlides
        size_tick = SizeTickSlides
        size_title = SizeTitleSlides
    elif output == 'paper':
        size_label = SizeLabelPaper
        size_tick = SizeTickPaper
        size_title = SizeTitlePaper
    else:
        raise ValueError

    params = {
        'axes.labelsize': size_label,
        'axes.titlesize': size_label,
        'figure.titlesize': size_title,
        'xtick.labelsize': size_tick,
        'ytick.labelsize': size_tick,
        'legend.fontsize': size_label,
        'legend.title_fontsize': size_title,
    }
    mpl.pyplot.rcParams.update(params)
    mpl.rc('font', **{'size': size_label})
    mpl.rc('text', usetex=True)

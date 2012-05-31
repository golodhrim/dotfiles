from libqtile.manager import Key, Click, Drag, Screen, Group
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

mod="mod4"
alt="mod1"

class Commands(object):
    dmenu = 'dmenu_run -i -b -p ">" -fn "Open Sans" -nb "#000" -nf "#fff" -sb "#15181a" -sf "#fff"'
    lock_screen = 'alock -auth pam -bg image:file=/home/golodhrim/.config/bg/somberwald.jpg:scale'
    screenshot = "scrot '%Y-%m-%d_$wx$h_qtile.png'"
    volume_up = 'amixer -q -c 0 sset Master 2dB+'
    volume_down = 'amixer -q -c 0 sset Master 2dB-'
    volume_toggle = 'amixer -q -c 0 sset Master toggle'

class Theme(object):
    bar = {
        'size': 24,
        'background': '000000',
        }
    widget = {
        'font': 'Open Sans',
        'fontsize': 11,
        'background': bar['background'],
        'foreground': 'eeeeee',
        }
    graph = {
        'background': '000000',
        'border_width': 0,
        'border_color': '000000',
        'margin_x': 0,
        'margin_y': 0,
        'width':50,
        }

    groupbox = widget.copy()
    groupbox.update({
        'padding': 2,
        'borderwidth': 3,
        })

    sep = {
        'background': bar['background'],
        'foreground': '444444',
        'height_percent': 75,
        }

    systray = widget.copy()
    systray.update({
        'icon_size': 16,
        'padding': 3,
        })

    battery = widget.copy()
    battery_text = battery.copy()
    battery_text.update({
        'format': '{char}{hour:d}:{min:02d}',
        })

keys = [
    Key(
        [mod], "k",
        lazy.layout.down()
    ),
    Key(
        [mod], "j",
        lazy.layout.up()
    ),
    Key(
        [mod, "control"], "k",
        lazy.layout.shuffle_down()
    ),
    Key(
        [mod, "control"], "j",
        lazy.layout.shuffle_up()
    ),
    Key(
        [mod], "i",
        lazy.layout.grow()
    ),
    Key(
        [mod], "m",
        lazy.layout.shrink()
    ),
    Key(
        [mod], "n",
        lazy.layout.normalize()
    ),
    Key(
        [mod], "o",
        lazy.layout.maximize()
    ),
    Key(
        [mod], "space",
        lazy.layout.next()
    ),
    Key(
        [mod, "shift"], "space",
        lazy.layout.rotate()
    ),
    Key(
        [mod, "shift"], "Return",
        lazy.layout.toggle_split()
    ),
    Key([mod], "h",      lazy.to_screen(1)),
    Key([mod], "l",      lazy.to_screen(0)),
    Key([mod], "Return", lazy.spawn("urxvtc")),
    Key([mod], "Tab",    lazy.nextlayout()),
    Key([mod], "w",      lazy.window.kill()),

    Key([mod, "control"], "p",      lazy.spawn(Commands.dmenu)),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn(Commands.volume_up)),
    Key([mod], "equal", lazy.spawn(Commands.volume_up)),
    Key([], 'XF86AudioLowerVolume', lazy.spawn(Commands.volume_down)),
    Key([mod], "minus", lazy.spawn(Commands.volume_down)),
    Key([], 'XF86AudioMute', lazy.spawn(Commands.volume_toggle)),
    Key([mod], 's', lazy.spawn(Commands.screenshot)),
    Key([mod, 'shift'], 's', lazy.spawn(Commands.lock_screen)),
    
    Key([mod], 'c', lazy.spawn('google-chrome')),
    Key([alt, "shift"], 'e', lazy.spawn('emacs')),
    
    Key([mod, "control"], "r", lazy.restart()),
]

group_setup = (
    ('sys', {
        'layout': 'tile',
        }),
    ('web', {
        'layout': 'floating',
        'apps': {'wm_class': ('Google-chrome', 'emacs')},
        }),
    ('IM', {
        'layout': 'max',
        'apps': {'wm_class': ('pidgin')},
        }),
    ('emacs', {
        'layout': 'max',
        'apps': {'wm_class': ('emacs')},
        }),
    ('office', {
        'layout': 'floating',
        }),
    ('stats', {
        'layout': 'tile',
        }),
    ('media', {
        'layout': 'floating',
        'apps': {'wm_class': ('mplayer2', 'mplayer')},
        }),
    ('etc', {}),
)

groups = []

for idx, (name, config) in enumerate(group_setup):
    hotkey = str(idx+1)
    groups.append(Group(name, layout=config.get('layout', 'tile')))
    keys.append(Key([alt], hotkey, lazy.group[name].toscreen()))
    keys.append(Key([alt, 'shift'], hotkey, lazy.window.togroup(name)))

layouts = [
    layout.Max(),
    layout.Stack(stacks=2),
    layout.RatioTile(),
    layout.TreeTab(),
    layout.Tile(tiles=2),
    layout.Floating(),
    layout.MonadTall(),
]

screens = [
    Screen(
        top = bar.Bar(
            [
                widget.GroupBox(**Theme.groupbox),
                widget.WindowName(**Theme.widget),
                widget.Volume(theme_path='/usr/share/icons/gnome/24x24/status/', **Theme.widget),
                widget.Battery(
                    energy_now_file='charge_now',
                    energy_full_file='charge_full',
                    power_now_file='current_now',
                    **Theme.battery_text
                ),
                widget.Systray(**Theme.systray),
                widget.Clock('%a %m/%d/%Y %I:%M %p', **Theme.widget),
             ], **Theme.bar),
        bottom = bar.Bar(
                    [
                        widget.TextBox('default', 'eth0:', **Theme.widget),
                        widget.NetGraph(interface='eth0', **Theme.graph),
                        widget.Sep(**Theme.sep),
                        widget.TextBox('defalt', 'wlan0:', **Theme.widget),
                        widget.NetGraph(interface='wlan0', **Theme.graph),
                        widget.Sep(**Theme.sep),
                        widget.TextBox('default', 'MPD:', **Theme.widget),
                        widget.Mpd(host='localhost',port='6600',msg_nc='MPD offline', **Theme.widget),
                        widget.Sep(**Theme.sep),
                        widget.CPUGraph(**Theme.graph),
                        widget.Sep(**Theme.sep),
                        widget.CurrentLayout(**Theme.widget),
                    ], **Theme.bar),
    ),
]

main = None
follow_mouse_focus = True
cursor_warp = False

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([alt], "Button2", lazy.window.bring_to_front())
]

floating_layout = layout.floating.Floating(float_rules=[{'wmclass': x} for x in (
    'Download',
    'dropbox',
    'file_progress',
    'file-roller',
    'gimp',
    'pidgin',
    'skype',
    'Xephyr',
    )])

@hook.subscribe.client_new
def floating_dialogs(window):
    dialog = window.window.get_wm_type() == 'dialog'
    transient = window.window.get_wm_transient_for()
    if dialog or transient:
        window.floating = True

#def main(qtile):
#    from grouper import AppGrouper, Match
#
#    # Send apps to specified groups on window creation
#    AppGrouper(qtile, [{
#        'group': name,
#        'match': Match(**config['apps']),
#        } for name, config in group_setup if 'apps' in config])

@hook.subscribe.startup          
def runner():
     import subprocess
     
     """
     Run after qtile is started
     """

     # startup-script is simple a list of programs to run
     #subprocess.Popen('startup-script')

     # terminal programs behave weird with regards to window titles
     # we open them separately and in a defined order so that the
     # client_new hook has time to group them by the window title
     # as the window title for them is the same when they open

     subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])
     subprocess.Popen(['nitrogen', '--restore'])
     subprocess.Popen(['conky'])
     subprocess.Popen(['wpa_gui'])
     subprocess.Popen(['guake'])
     subprocess.Popen(['dropbox'])
     subprocess.Popen(['urxvtd', '-q', '-f', '-o'])
     subprocess.Popen(['emacs'])

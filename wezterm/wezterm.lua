local wezterm = require 'wezterm'
local config = {}

if wezterm.config_builder then
  config = wezterm.config_builder()
end

-- Fuente con ligaduras
config.font = wezterm.font('Fira Code', { weight = 'Regular' })
config.font_size = 13
config.harfbuzz_features = { 'calt=1', 'clig=1', 'liga=1' }

-- Fondo: GIF Matrix rain detrás del texto
config.background = {
  {
    source = { File = '/home/hector/.config/wezterm/matrix-rain.gif' },
    width = 'Cover',
    height = 'Cover',
    repeat_x = 'Mirror',
    repeat_y = 'Mirror',
    opacity = 0.6,
    hsb = {
      brightness = 0.8,
      saturation = 1.5,
    },
  },
  {
    source = { Color = '#0D0208' },
    width = '100%',
    height = '100%',
    opacity = 0.55,
  },
}

-- Colores Matrix
config.colors = {
  foreground = '#00FF41',
  background = '#0D0208',
  cursor_bg = '#00FF41',
  cursor_fg = '#000000',
  cursor_border = '#00FF41',
  selection_fg = '#000000',
  selection_bg = '#00FF41',

  ansi = {
    '#0D0208', -- black
    '#FF0033', -- red
    '#00FF41', -- green
    '#C7C329', -- yellow
    '#008F11', -- blue
    '#C839C5', -- magenta
    '#20C5C6', -- cyan
    '#00FF41', -- white
  },
  brights = {
    '#003B00', -- bright black
    '#FF3366', -- bright red
    '#33FF66', -- bright green
    '#66FF8C', -- bright yellow
    '#00CC33', -- bright blue
    '#FD7CFC', -- bright magenta
    '#68FDFE', -- bright cyan
    '#D4FFDA', -- bright white
  },

  tab_bar = {
    background = '#0D0208',
    active_tab = {
      bg_color = '#00FF41',
      fg_color = '#000000',
    },
    inactive_tab = {
      bg_color = '#0D0208',
      fg_color = '#00FF41',
    },
  },
}

-- Cursor parpadeante
config.default_cursor_style = 'BlinkingBlock'
config.cursor_blink_rate = 500

-- Ventana
config.window_padding = { left = 10, right = 10, top = 10, bottom = 10 }
config.window_background_opacity = 0.85
config.window_close_confirmation = 'NeverPrompt'
config.enable_tab_bar = true
config.hide_tab_bar_if_only_one_tab = true

-- Performance
config.animation_fps = 30
config.max_fps = 60

return config

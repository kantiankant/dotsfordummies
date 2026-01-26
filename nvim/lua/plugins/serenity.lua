local function apply_serenity()
  -- Register the name immediately to satisfy LazyVim's check
  vim.g.colors_name = "serenity"

  vim.o.termguicolors = true
  local colors = {
    panel = "NONE", -- Transparent
    fg = "#FFFFFF", -- Primary text (Pure White)
    bright_white = "#FFFFFF",

    -- High-contrast syntax colors
    blue = "#89B4FA",
    magenta = "#CBA6F7",
    green = "#A6E3A1",
    yellow = "#F9E2AF",
    cyan = "#94E2D5",
    red = "#F38BA8",

    -- UI elements
    border = "#444444",
    dim_text = "#888888", -- For line numbers and comments
  }

  local function set(g, o)
    vim.api.nvim_set_hl(0, g, o)
  end

  -- Clear existing highlights
  vim.cmd("highlight clear")

  -- Core Editor & Transparency
  set("Normal", { fg = colors.fg, bg = colors.panel })
  set("NormalNC", { fg = colors.fg, bg = colors.panel })
  set("SignColumn", { bg = colors.panel })
  set("LineNr", { fg = colors.dim_text, bg = colors.panel })
  set("CursorLineNr", { fg = colors.white, bold = true })
  set("NormalFloat", { fg = colors.fg, bg = colors.panel })
  set("FloatBorder", { fg = colors.border, bg = colors.panel })

  -- Syntax (Brightened)
  set("Comment", { fg = colors.dim_text, italic = true })
  set("String", { fg = colors.green })
  set("Function", { fg = colors.blue, bold = true })
  set("Keyword", { fg = colors.magenta, bold = true })
  set("Statement", { fg = colors.magenta })
  set("Type", { fg = colors.yellow })
  set("Constant", { fg = colors.red })
  set("Special", { fg = colors.cyan })

  -- Treesitter
  set("@variable", { fg = colors.white })
  set("@variable.builtin", { fg = colors.red, italic = true })
  set("@function", { link = "Function" })
  set("@keyword", { link = "Keyword" })
  set("@property", { fg = colors.cyan })
  set("@parameter", { fg = colors.white, italic = true })
end

return {
  -- 1. Tell LazyVim to use our theme
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "serenity",
    },
  },

  -- 2. Register the theme so Neovim "finds" it
  {
    "serenity-theme",
    dir = vim.fn.stdpath("config"),
    priority = 1000,
    lazy = false,
    config = function()
      apply_serenity()
    end,
  },
}

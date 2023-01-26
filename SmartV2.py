import neovim
from openai import OpenAI

@neovim.plugin
class ChatGPTFixer(object):
    def __init__(self, vim):
        self.vim = vim
        self.openai = OpenAI(api_key="your_api_key_here")
        self.menu_options = []

    @neovim.command("ChatGPTFix", range='', nargs='*', sync=True)
    def chatgpt_fix(self, args, range):
        current_line = self.vim.current.line
        suggestions = self.openai.Completion.create(
            prompt=current_line,
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        self.menu_options = [suggestion["text"] for suggestion in suggestions["choices"]]
        self.vim.call("coc#util#create_menu", self.menu_options)

    @neovim.function("ChatGPTFixMenu", sync=True)
    def chatgpt_fix_menu(self, args):
        self.vim.command("ChatGPTFix")

    @neovim.function("ChatGPTFixApply", sync=True)
    def chatgpt_fix_apply(self, args):
        menu_index = self.vim.call("coc#util#input", "Enter the index of the suggestion to apply: ")
        if not menu_index.isdigit() or int(menu_index) > len(self.menu_options):
            self.vim.out_write("Invalid index\n")
            return

        self.vim.current.line = self.menu_options[int(menu_index)]

    @neovim.autocmd("CursorMovedI", pattern="*", sync=True)
    def on_cursor_moved(self):
        self.chatgpt_fix_menu(None)


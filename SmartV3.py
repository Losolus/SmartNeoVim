import neovim
import json
import requests

@neovim.plugin
class ChatGPT(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.command('ChatGPT', range='', nargs='*', sync=True)
    def chatgpt(self, args, range):
        # Create a new buffer
        self.nvim.command("new")
        self.nvim.command("setlocal buftype=nofile")
        self.nvim.command("setlocal bufhidden=wipe")
        self.nvim.command("setlocal noswapfile")
        self.nvim.command("setlocal nowrap")
        self.nvim.command("setlocal nonumber")
        self.nvim.command("setlocal norelativenumber")
        self.nvim.command("setlocal noai")
        self.nvim.command("setlocal nocursorline")
        self.nvim.command("setlocal nocursorcolumn")
        self.nvim.command("setlocal foldcolumn=0")

        # Set the buffer's name
        self.nvim.command("file ChatGPT")

        # Append the initial text
        self.nvim.current.buffer.append("Start chatting with ChatGPT:")

        # Add highlighting
        self.nvim.command('highlight default link Question Question')

        self.nvim.input_str('i')
        self.nvim.feedkeys(':setlocal keymap=i<CR>', 'n')

    @neovim.function('send_query', sync=True)
    def send_query(self, args):
        query = args[0]
        API_KEY = "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"
        API_URL = "https://api.openai.com/v1/engines/davinci-codex/completions"
        data = {
            "prompt": query,
            "temperature": 0.5,
            "max_tokens": 2048
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + API_KEY
        }

        response = requests.post(API_URL, json=data, headers=headers)

        # check if the API call was successful
        if response.status_code != 200:
            self.nvim.current.buffer.append("Error: " + str(response.status_code))
        else:
            # extract the ChatGPT response
            response_data = json.loads(response.text)
            chatgpt_response = response_data["choices"][0]["text"]

            # append the ChatGPT response to the buffer
            self.nvim.current.buffer.append("ChatGPT: " + chatgpt_response)
            self.nvim.command('highlight default link ChatGPT ChatGPT')

            self.nvim.command("startinsert")


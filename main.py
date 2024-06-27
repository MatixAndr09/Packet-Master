import requests
from textual import *

class APIClientApp(App):
    async def on_mount(self):
        # Header
        header = Header()
        await self.view.dock(header, edge="top")

        # Footer
        footer = Footer()
        await self.view.dock(footer, edge="bottom")

        # Main layout in a grid
        grid = await self.view.dock(GridView(), edge="left")

        # GET request section
        self.url_input = Input(placeholder="Enter URL", name="url")
        self.url_input.value = "http://jsonplaceholder.typicode.com/posts"
        self.method_label = Static("GET", name="method")
        self.send_button = Button("Send", name="send")

        # Parameters section
        self.params_input = Input(placeholder="Parameters (key=value)", name="params")
        self.params_input.value = "foo=bar&bar=baz&something=value"

        # Headers section
        self.headers_input = Input(placeholder="Headers (key=value)", name="headers")
        self.headers_input.value = "Content-Type=application/json"

        # Response section
        self.response_log = TextLog(name="response")

        # Adding to the grid
        await grid.add_column("col", max_size=30, fraction=1)
        await grid.add_row("row", max_size=3)
        await grid.add_row("row", max_size=3)
        await grid.add_row("row", max_size=3)
        await grid.add_row("row", fraction=1)
        await grid.add_areas(
            area1="col,row",
            area2="col,row",
            area3="col,row",
            area4="col,row",
        )
        await grid.place(area1=self.url_input, area2=self.params_input, area3=self.headers_input, area4=self.send_button)
        await grid.place(area4=self.response_log)
        
        self.send_button.on_click = self.send_request

    async def send_request(self):
        url = self.url_input.value
        params = dict(item.split("=") for item in self.params_input.value.split("&"))
        headers = dict(item.split("=") for item in self.headers_input.value.split("&"))

        response = requests.get(url, params=params, headers=headers)
        self.response_log.write(f"Response Code: {response.status_code}\n")
        for key, value in response.headers.items():
            self.response_log.write(f"{key}: {value}\n")

if __name__ == "__main__":
    APIClientApp.run()

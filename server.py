from api.config.config import DevConfig
from api import create_app


app = create_app(DevConfig)

if __name__ == "__main__":
    app.run()
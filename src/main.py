import logging
import sys

from app import App

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(stream=sys.stderr),
    ],
    format="[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

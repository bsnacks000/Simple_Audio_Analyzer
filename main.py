#!usr/env/bin python

from Controller import Controller


def main():
    """
    Runs the app and handles non-graceful closing via the GUI window.
    """

    app = Controller()

    app.geometry('500x500+300+200')
    app.title('Simple Audio Analyzer')

    def on_closing():
        app.quit()    # need this to fully close if window is exited... shuts down all processes

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()


if __name__ == '__main__':
    main()
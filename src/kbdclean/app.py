import sys

from PyQt6.QtWidgets import QApplication, QMessageBox

from kbdclean.grabber import KeyboardGrabber, KbdCleanPermissionError
from kbdclean.phrase import PhraseDetector
from kbdclean.window import MainWindow
from kbdclean.worker import KeyboardWorker


def main() -> None:
    app = QApplication(sys.argv)

    grabber = KeyboardGrabber()
    try:
        grabber.discover()
    except KbdCleanPermissionError as e:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("kbdclean — Permission Error")
        msg.setText(str(e))
        msg.exec()
        return

    if not grabber.devices:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("kbdclean — No Keyboards Found")
        msg.setText("No keyboard devices were found on this system.")
        msg.exec()
        return

    grabber.grab_all()

    detector = PhraseDetector()
    workers = [KeyboardWorker(dev, detector) for dev in grabber.devices]

    window = MainWindow(workers)  # noqa: F841

    for worker in workers:
        worker.start()

    app.exec()

    grabber.ungrab_all()
    sys.exit(0)

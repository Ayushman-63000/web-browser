import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLineEdit, QPushButton, QToolBar, QLabel, QMessageBox, QTabBar, QAction
from PyQt5.QtCore import QUrl, Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont, QPainter, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Browser")

        # Initialize webviews and current tab index
        self.webviews = []
        self.current_tab_index = 0

        # Create main UI elements
        self.create_ui()

    def create_ui(self):
        # Set the main window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QToolBar {
                background-color: #ffffff;
                border: 1px solid #ddd;
            }
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #ddd;
                padding: 5px 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #ddd;
                padding: 5px 10px;
                font-size: 14px;
            }
            QTabBar::tab {
                background-color: #ffffff;
                border: 1px solid #ddd;
                padding: 5px 10px;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background-color: #f0f0f0;
                border-bottom-color: #f0f0f0;
            }
            QTabBar::close-button {
                image: url(close.png);
                subcontrol-origin: padding;
                subcontrol-position: right;
                padding-right: 4px;
            }
            QTabBar::close-button:hover {
                background-color: #e0e0e0;
            }
        """)

        # Create a toolbar
        self.toolbar = QToolBar("Navigation")
        self.addToolBar(self.toolbar)

        # Create navigation buttons
        self.back_button = QPushButton("←")
        self.back_button.clicked.connect(self.go_back)
        self.toolbar.addWidget(self.back_button)

        self.forward_button = QPushButton("→")
        self.forward_button.clicked.connect(self.go_forward)
        self.toolbar.addWidget(self.forward_button)

        self.refresh_button = QPushButton("↻")
        self.refresh_button.clicked.connect(self.refresh_page)
        self.toolbar.addWidget(self.refresh_button)

        self.home_button = QPushButton("🏠")
        self.home_button.clicked.connect(self.go_home)
        self.toolbar.addWidget(self.home_button)

        self.new_tab_button = QPushButton("+")
        self.new_tab_button.clicked.connect(self.new_tab)
        self.toolbar.addWidget(self.new_tab_button)

        # Create a tab widget for tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tab_widget)
        self.tab_widget.currentChanged.connect(self.on_tab_change)

        # Create the address bar
        self.url_entry = QLineEdit()
        self.url_entry.returnPressed.connect(self.load_url)
        self.toolbar.addWidget(self.url_entry)

        self.load_button = QPushButton("Go")
        self.load_button.clicked.connect(self.load_url)
        self.toolbar.addWidget(self.load_button)

        # Create the first tab
        self.new_tab()

    def new_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        webview = QWebEngineView()
        webview.setUrl(QUrl("https://www.google.com"))
        layout.addWidget(webview)

        self.webviews.append(webview)
        self.tab_widget.addTab(tab, f"Tab {len(self.webviews)}")

        # Update the current tab index
        self.current_tab_index = len(self.webviews) - 1

    def close_tab(self, index):
        if len(self.webviews) > 1:
            self.tab_widget.removeTab(index)
            del self.webviews[index]
            if index == self.current_tab_index:
                self.current_tab_index = max(0, index - 1)
        else:
            QMessageBox.warning(self, "Warning", "You cannot close the last tab.")

    def on_tab_change(self, index):
        self.current_tab_index = index
        if index != -1:
            webview = self.webviews[index]
            self.url_entry.setText(webview.url().toString())

    def load_url(self):
        url = self.url_entry.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        webview = self.webviews[self.current_tab_index]
        webview.setUrl(QUrl(url))

    def go_back(self):
        webview = self.webviews[self.current_tab_index]
        webview.back()

    def go_forward(self):
        webview = self.webviews[self.current_tab_index]
        webview.forward()

    def refresh_page(self):
        webview = self.webviews[self.current_tab_index]
        webview.reload()

    def go_home(self):
        self.url_entry.setText("https://www.google.com")
        self.load_url()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMessageBox {
            background-color: #ffffff;
            color: #000000;
            font-size: 14px;
        }
        QMessageBox QPushButton {
            background-color: #f0f0f0;
            border: 1px solid #ddd;
            padding: 5px 10px;
            font-size: 14px;
        }
        QMessageBox QPushButton:hover {
            background-color: #e0e0e0;
        }
    """)

    browser = SimpleBrowser()
    browser.showMaximized()
    sys.exit(app.exec_())
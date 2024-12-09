from sys import argv
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView #Web Browser (HTML Frame)
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineSettings


class SplashScreen(QSplashScreen):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setMask(pixmap.mask())

class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        # Create a splash screen with your logo
        splash_pix = QPixmap("C:/Users/RAJEEV/3D Objects/imp doc/python/web browsercopy/logo1.png")
        self.splash = SplashScreen(splash_pix)
        self.splash.show()
        
        # Setup timer to close splash screen and show main window
        QTimer.singleShot(2000, self.show_main_window)

    def show_main_window(self):
        self.splash.close()    

        self.setWindowIcon(QIcon("C:/Users/RAJEEV/3D Objects/imp doc/python/web browsercopy/icon.png"))
        
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://www.google.com'))
        self.browser.urlChanged.connect(self.update_AddressBar)
        self.setCentralWidget(self.browser)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.navigation_bar = QToolBar('Navigation Toolbar')
        self.addToolBar(self.navigation_bar)

        back_button = QPushButton(QIcon('C:/Users/RAJEEV/3D Objects/imp doc/python/web browsercopy/icon3.png'), "", self)
        back_button.setStatusTip('Go to the previous page you visited')
        back_button.clicked.connect(self.browser.back)
        self.navigation_bar.addWidget(back_button)

        refresh_button = QPushButton(QIcon('C:/Users/RAJEEV/3D Objects/imp doc/python/web browsercopy/icon5.png'), "", self)
        refresh_button.setStatusTip('Refresh this page')
        refresh_button.clicked.connect(self.browser.reload)
        self.navigation_bar.addWidget(refresh_button)

        forward_button = QPushButton(QIcon('C:/Users/RAJEEV/3D Objects/imp doc/python/web browsercopy/icon6.png'), "", self)
        forward_button.setStatusTip('Go to the next page')
        forward_button.clicked.connect(self.browser.forward)
        self.navigation_bar.addWidget(forward_button)

        home_button = QPushButton(QIcon('C:/Users/RAJEEV/3D Objects/imp doc/python/web browsercopy/icon4.png'), "", self) 
        home_button.setStatusTip('Go to the home page (Google page)')
        home_button.clicked.connect(self.go_to_home)
        self.navigation_bar.addWidget(home_button)

        theme_button = QPushButton(self)
        theme_button.setIcon(QIcon("C:/Users/RAJEEV/3D Objects/imp doc/python/web browsercopy/icon2.png"))  # Provide the path to your icon file
        theme_button.setStatusTip('Toggle between dark and light themes')
        theme_button.clicked.connect(self.toggle_theme)
        self.navigation_bar.addWidget(theme_button)

        self.URLBar = QLineEdit()
        self.URLBar.returnPressed.connect(self.navigate_to_url)  # Connect returnPressed signal to navigate_to_url method
        self.navigation_bar.addWidget(self.URLBar)

        self.addToolBarBreak()

        # Adding another toolbar which contains the bookmarks
        bookmarks_toolbar = QToolBar('Bookmarks', self)
        self.addToolBar(bookmarks_toolbar)

        facebook = QAction("Facebook", self)
        facebook.setStatusTip("Go to Facebook")
        facebook.triggered.connect(lambda: self.go_to_URL(QUrl("https://www.facebook.com")))
        bookmarks_toolbar.addAction(facebook)

        linkedin = QAction("LinkedIn", self)
        linkedin.setStatusTip("Go to LinkedIn")
        linkedin.triggered.connect(lambda: self.go_to_URL(QUrl("https://in.linkedin.com")))
        bookmarks_toolbar.addAction(linkedin)

        instagram = QAction("Instagram", self)
        instagram.setStatusTip("Go to Instagram")
        instagram.triggered.connect(lambda: self.go_to_URL(QUrl("https://www.instagram.com")))
        bookmarks_toolbar.addAction(instagram)

        twitter = QAction("Twitter", self)
        twitter.setStatusTip('Go to Twitter')
        twitter.triggered.connect(lambda: self.go_to_URL(QUrl("https://www.twitter.com")))
        bookmarks_toolbar.addAction(twitter)

        
        # Disable caching
        self.browser.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, False)
        self.browser.settings().setAttribute(QWebEngineSettings.LocalStorageDatabaseEnabled, False)
        self.browser.settings().setAttribute(QWebEngineSettings.OfflineStorageDatabaseEnabled, False)
        self.browser.settings().setAttribute(QWebEngineSettings.DnsPrefetchEnabled, False)

        # Disable autofill
        self.URLBar.setEchoMode(QLineEdit.Normal)
        self.URLBar.setClearButtonEnabled(False)

        # Disable tracking (disable JavaScript execution and block third-party cookies)
        self.browser.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, False)
        self.browser.settings().setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, False)
        self.browser.settings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, False)
        self.browser.settings().setAttribute(QWebEngineSettings.JavascriptCanCloseWindows, False)
        self.browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, False)
        self.browser.settings().setAttribute(QWebEngineSettings.CookieEnabled, False)
        self.browser.settings().setAttribute(QWebEngineSettings.ThirdPartyCookiesEnabled, False)

        # Remaining code for toolbar, bookmarks, etc. remains the same


        self.showMaximized()
        self.show()


    def go_to_home(self):
     self.browser.setUrl(QUrl('https://www.duckduckgo.com/'))

    def go_to_URL(self, url: QUrl):
     if url.scheme() == '':
        url.setScheme('https://')
     self.browser.setUrl(url)
     self.update_AddressBar(url)

    def update_AddressBar(self, url):
     self.URLBar.setText(url.toString())
     self.URLBar.setCursorPosition(0)
     
    def toggle_theme(self):
        current_theme = self.styleSheet()
        if 'dark' in current_theme:
            # Switch to light theme
            self.setStyleSheet('')
        else:
            # Switch to dark theme
            self.setStyleSheet('''
                /* Your dark theme stylesheet here */
                background-color: #2E2F30;
                color: #FFFFFF;
            ''')
    
    def navigate_to_url(self):
        text = self.URLBar.text().strip()
        if '.' in text and ' ' not in text:
            if text.startswith(('http://', 'https://')):
                url = QUrl(text)
            
            else:
                url = QUrl('https://www.' + text)
            self.go_to_URL(url)
        else:
            search_url = QUrl('https://www.google.com/search?q=' + text)
            self.go_to_URL(search_url)


app = QApplication(argv)
app.setApplicationName('Browser')

window = Window()
app.exec_()
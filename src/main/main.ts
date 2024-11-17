import { app, BrowserWindow, ipcMain, session } from 'electron';
import { join } from 'path';

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    }
  });

  // Hide the menu bar
  mainWindow.setMenuBarVisibility(false);
  mainWindow.setAutoHideMenuBar(true);

  // Open DevTools automatically
  mainWindow.webContents.openDevTools();

  if (process.env.NODE_ENV === 'development') {
    const rendererPort = process.argv[2];
    mainWindow.loadURL(`http://localhost:${rendererPort}`);
  } else {
    mainWindow.loadFile(join(app.getAppPath(), 'renderer', 'index.html'));
  }

  // Log when the window is ready to show
  mainWindow.once('ready-to-show', () => {
    console.log('Window is ready to show');
    mainWindow.show();
  });

  // Defer heavy tasks
  setTimeout(() => {
    console.log('Performing heavy tasks');
    // Perform heavy tasks here
  }, 1000);
}

app.whenReady().then(() => {
  createWindow();

  session.defaultSession.webRequest.onHeadersReceived((details, callback) => {
    callback({
      responseHeaders: {
        ...details.responseHeaders,
        'Content-Security-Policy': ['script-src \'self\'']
      }
    })
  })

  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
});

ipcMain.on('message', (_, message) => {
  console.log(message);
});
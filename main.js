const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');

function createWindow() {
  const win = new BrowserWindow({
    width: 1600,
    height: 960,
    minWidth: 1200,
    minHeight: 700,
    backgroundColor: '#0a0f1e',
    titleBarStyle: 'hiddenInset',
    frame: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    },
    icon: path.join(__dirname, 'assets', 'icon.png')
  });

  win.loadFile('index.html');

  // Window controls
  ipcMain.on('window-minimize', () => win.minimize());
  ipcMain.on('window-maximize', () => {
    if (win.isMaximized()) win.unmaximize();
    else win.maximize();
  });
  ipcMain.on('window-close', () => win.close());
}

// Parse CSV helper
function parseCSV(filePath) {
  return new Promise((resolve, reject) => {
    const results = [];
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.trim().split('\n');
    const headers = lines[0].replace(/\r/g, '').split(',');
    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].replace(/\r/g, '').split(',');
      if (values.length < headers.length) continue;
      const row = {};
      headers.forEach((h, idx) => { row[h.trim()] = values[idx] ? values[idx].trim() : ''; });
      results.push(row);
    }
    resolve(results);
  });
}

function parseCSVFromString(text) {
  const lines = text.trim().split('\n');
  const headers = lines[0].replace(/\r/g, '').split(',').map(h => h.trim());

  return lines.slice(1).map(line => {
    const values = line.replace(/\r/g, '').split(',');
    const row = {};
    headers.forEach((h, i) => {
      row[h] = values[i] ? values[i].trim() : '';
    });
    return row;
  });
}

// python algorithm runner
ipcMain.handle('run-algorithm', async (event, repoData) => {
  const inputPath = path.join(__dirname, 'temp_repo.csv');
  const outputPath = path.join(__dirname, 'temp_results.csv');

  // Save uploaded repo data
  const csv = Object.keys(repoData[0]).join(',') + '\n' +
    repoData.map(r => Object.values(r).join(',')).join('\n');

  fs.writeFileSync(inputPath, csv);

  return new Promise((resolve, reject) => {
    exec(`python algorithm.py`, (err) => {
      if (err) return reject(err);

      const results = fs.readFileSync('beam_results.csv', 'utf-8');
      resolve(parseCSVFromString(results));
    });
  });
});

// IPC: load beam results
ipcMain.handle('load-results', async () => {
  try {
    const resultsPath = path.join(__dirname, 'data', 'beam_results.csv');
    const repoPath = path.join(__dirname, 'data', 'Beam_Repository_DATA.csv');
    const results = await parseCSV(resultsPath);
    const repo = await parseCSV(repoPath);
    return { results, repo };
  } catch (err) {
    return { error: err.message };
  }
});

// IPC: export data
ipcMain.handle('export-data', async (event, { data, filename }) => {
  const { filePath } = await dialog.showSaveDialog({
    defaultPath: filename,
    filters: [{ name: 'CSV', extensions: ['csv'] }]
  });
  if (filePath) {
    fs.writeFileSync(filePath, data);
    return { success: true };
  }
  return { success: false };
});

app.whenReady().then(createWindow);
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); });
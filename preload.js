const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  runAlgorithm: (Data) => ipcRenderer.invoke('run-algorithm', Data),
  loadData: () => ipcRenderer.invoke('load-results'),
  exportData: (payload) => ipcRenderer.invoke('export-data', payload),
  minimize: () => ipcRenderer.send('window-minimize'),
  maximize: () => ipcRenderer.send('window-maximize'),
  close: () => ipcRenderer.send('window-close')
});
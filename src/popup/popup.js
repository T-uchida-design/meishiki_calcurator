document.addEventListener('DOMContentLoaded', async () => {
  const titleElement = document.getElementById('title');
  const urlElement = document.getElementById('url');
  const copyButton = document.getElementById('copyButton');
  const statusElement = document.getElementById('status');

  // 現在のタブの情報を取得
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  // タイトルとURLを表示
  titleElement.textContent = tab.title;
  urlElement.textContent = tab.url;

  // コピーボタンのクリックイベント
  copyButton.addEventListener('click', async () => {
    const textToCopy = `${tab.title}\n${tab.url}`;
    
    try {
      await navigator.clipboard.writeText(textToCopy);
      statusElement.textContent = 'コピーしました！';
      
      // 3秒後にステータスメッセージを消す
      setTimeout(() => {
        statusElement.textContent = '';
      }, 3000);
    } catch (err) {
      statusElement.textContent = 'コピーに失敗しました';
      console.error('コピーに失敗しました:', err);
    }
  });
}); 
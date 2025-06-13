// ページの背景色を設定
document.body.style.backgroundColor = '#FFF0F5';

// すべてのボタンのスタイルをカスタマイズ
const styleButtons = () => {
  const buttons = document.getElementsByTagName('button');
  for (let button of buttons) {
    button.style.backgroundColor = '#FFB6C1';
    button.style.border = '2px solid #FF69B4';
    button.style.borderRadius = '15px';
    button.style.padding = '8px 16px';
    button.style.color = '#333';
    button.style.transition = 'all 0.3s ease';
  }
};

// ページ読み込み完了時に実行
window.addEventListener('load', () => {
  styleButtons();
});

// DOMの変更を監視して新しいボタンにもスタイルを適用
const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    if (mutation.addedNodes.length) {
      styleButtons();
    }
  });
});

observer.observe(document.body, {
  childList: true,
  subtree: true
}); 
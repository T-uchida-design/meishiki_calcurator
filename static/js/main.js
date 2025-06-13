document.getElementById('birthForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const birthDate = document.getElementById('birth_date').value;
    const birthTime = document.getElementById('birth_time').value;
    
    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                birth_date: birthDate,
                birth_time: birthTime
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            const resultContainer = document.getElementById('result');
            resultContainer.innerHTML = `
                <h2>計算結果</h2>
                <p>和暦：${data.wareki}</p>
                <!-- 他の結果もここに追加 -->
            `;
            resultContainer.classList.add('show');
        } else {
            alert('エラーが発生しました：' + data.error);
        }
    } catch (error) {
        alert('エラーが発生しました：' + error.message);
    }
}); 
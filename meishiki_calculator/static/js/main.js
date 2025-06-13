document.getElementById('birthForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const birthDate = document.getElementById('birth_date').value;
    
    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                birth_date: birthDate
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            const resultContainer = document.getElementById('result');
            resultContainer.innerHTML = `
                <h2>計算結果</h2>
                <p>生年月日：${data.birth_date}</p>
                <p>和暦：${data.wareki}</p>
                <h3>命式</h3>
                <div class="meishiki-grid">
                    <div class="meishiki-item">
                        <h4>年柱</h4>
                        <p>${data.meishiki.year}</p>
                    </div>
                    <div class="meishiki-item">
                        <h4>月柱</h4>
                        <p>${data.meishiki.month}</p>
                    </div>
                    <div class="meishiki-item">
                        <h4>日柱</h4>
                        <p>${data.meishiki.day}</p>
                    </div>
                </div>
            `;
            resultContainer.classList.add('show');
        } else {
            alert('エラーが発生しました：' + data.error);
        }
    } catch (error) {
        alert('エラーが発生しました：' + error.message);
    }
}); 
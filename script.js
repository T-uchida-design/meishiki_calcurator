document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // フォームデータの取得
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            subject: document.getElementById('subject').value,
            message: document.getElementById('message').value
        };

        // バリデーション
        if (!validateForm(formData)) {
            return;
        }

        // 送信処理（ここではコンソールに出力）
        console.log('送信されたデータ:', formData);
        
        // 送信成功メッセージ
        alert('お問い合わせありがとうございます。\n内容を確認次第、ご連絡させていただきます。');
        
        // フォームのリセット
        form.reset();
    });

    function validateForm(data) {
        // 名前のバリデーション
        if (data.name.trim() === '') {
            alert('お名前を入力してください。');
            return false;
        }

        // メールアドレスのバリデーション
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(data.email)) {
            alert('有効なメールアドレスを入力してください。');
            return false;
        }

        // 件名のバリデーション
        if (data.subject.trim() === '') {
            alert('件名を入力してください。');
            return false;
        }

        // メッセージのバリデーション
        if (data.message.trim() === '') {
            alert('お問い合わせ内容を入力してください。');
            return false;
        }

        return true;
    }
}); 
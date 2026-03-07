function copy(id) {
    const text = document.getElementById(id).innerText;
    navigator.clipboard.writeText(text).then(() => {
        // マイクラの「経験値オーブ」を拾った時のような音を出せると最高ですが、まずはアラートで。
        const btn = event.target;
        const originalText = btn.innerText;
        btn.innerText = "OK!";
        btn.style.backgroundColor = "#5ea818";
        
        setTimeout(() => {
            btn.innerText = originalText;
            btn.style.backgroundColor = "#c6c6c6";
        }, 1500);
    });
}

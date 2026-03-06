<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>しろくま鯖 | Minecraft Server Official</title>
    <style>
        :root { --main-blue: #00b4d8; --soft-white: #f8f9fa; }
        body { font-family: 'Helvetica Neue', Arial, sans-serif; background-color: var(--soft-white); margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; max-width: 500px; width: 90%; }
        h1 { color: var(--main-blue); font-size: 2rem; margin-bottom: 10px; }
        .server-status { color: #666; font-size: 0.9rem; margin-bottom: 20px; }
        .ip-card { background: #edf2f4; padding: 15px; border-radius: 10px; border: 2px dashed var(--main-blue); position: relative; cursor: pointer; transition: 0.3s; }
        .ip-card:hover { background: #e2eafc; }
        .copy-hint { font-size: 0.7rem; color: var(--main-blue); margin-top: 5px; }
        .btn { display: inline-block; margin-top: 25px; padding: 12px 25px; background-color: var(--main-blue); color: white; text-decoration: none; border-radius: 30px; font-weight: bold; transition: 0.3s; }
        .btn:hover { opacity: 0.8; transform: translateY(-2px); }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐾 しろくま鯖 🐾</h1>
        <p class="server-status">アットホームなサバイバルサーバー</p>
        
        <div class="ip-card" onclick="copyIP()">
            <div id="ip-address">play.sirokuma-saba.example</div>
            <div class="copy-hint">クリックしてIPをコピー</div>
        </div>

        <p>初心者大歓迎！みんなで仲良くマイクラを楽しもう。</p>
        
        <a href="#" class="btn">Discordに参加する</a>
    </div>

    <script>
        function copyIP() {
            const ip = document.getElementById('ip-address').innerText;
            navigator.clipboard.writeText(ip);
            alert("IPアドレスをコピーしました！：" + ip);
        }
    </script>
</body>
</html>

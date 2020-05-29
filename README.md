# LINE BOT

python,Flask,google cloud platformでline　botを作成します

簡単な会話、画像の保存、ニュースのスクレイピングができる
 
# DEMO
<img src="https://user-images.githubusercontent.com/53184634/83309508-6e496100-a244-11ea-9cf2-458521b6d8c4.png" width='400'>
![demo](https://user-images.githubusercontent.com/53184634/83309508-6e496100-a244-11ea-9cf2-458521b6d8c4.png)
# Requirement
 
requirements.txtで必要なモジュールを使えるようにしている

# Usage

- ファイルに必要事項を追加する
 - your backet name:GCSのbacket名を記入
 - YOUR_CHANNEL_ACCESS_TOKEN：LINEのアクセストークンを記入
 - YOUR_CHANNEL_SECRET：LINEのチャンネルシークレットを記入
 
google cloud consoleにファイルをアップロードして以下のコマンドを入力して実行する

- 初期化コマンド
```bash
gcloud init
```
- 実行コマンド
```bash
gcloud app deploy
```

#   A I o T _ H W 6 
## 1.前言
此專案為物聯網作業，使用ESP32連接DHT11，取得溫溼度資料，在樹莓派上用flask架設伺服器，接收溫溼度資料儲存資料到資料庫，並在網頁上渲染資料並動態更新。
## 2.Raspberry Pi 4 刷機
- 下載raspberry pi imager，並安裝到一張64GB記憶卡
- 下載後，開啟並選擇正確的版本後刷機
- 刷機完成後，將MicroSD卡放置到Rpi4背面，並接上電源線、螢幕連接線、鍵盤、滑鼠後，開機
- 開機後，進行初始化設定（設定名稱、密碼、時區等資訊）
- 將Rpi4連接網路（本次使用手機熱點）
## 3.取得溫溼度資料
- 在自己的電腦上開啟Adruino並將tempToDB.ino刷機入ESP32
- ESP32連接DHT11來獲取溫濕度數值
- 執行結果如下圖
- 可看到溫溼度資料已取得，但尚未開啟伺服器，因此還無法Post資料
## 4.架設伺服器與展現
- 開啟終端機執行以下指令
```
sudo apt update
sudo apt install python3
sudo apt install python3-pip
sudo pip3 install flask
```
## 5.參考資料
- https://github.com/sc0210/3311_Lab6_student

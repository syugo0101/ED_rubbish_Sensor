const bleno = require('@abandonware/bleno');
const fs = require('fs');

const SERVICE_UUID = '12345678-1234-5678-1234-56789abcdef0';
const CHARACTERISTIC_UUID = 'abcdef01-1234-5678-1234-56789abcdef0';

const SCORE_FILE_PATH = '/home/takeda/score_data.json'  // Python側と共有

class ScoreCharacteristic extends bleno.Characteristic {
  constructor() {
    super({
      uuid: CHARACTERISTIC_UUID,
      properties: ['read', 'write'],
      descriptors: [
        new bleno.Descriptor({
          uuid: '2901',
          value: 'Score Data JSON'
        })
      ]
    });
  }

  onReadRequest(offset, callback) {
    fs.readFile(SCORE_FILE_PATH, 'utf8', (err, data) => {
      if (err) {
        console.error('スコアファイル読み込み失敗:', err);
        return callback(this.RESULT_UNLIKELY_ERROR);
      }
      const buffer = Buffer.from(data, 'utf8');
      console.log('Read request received, sending score data');
      callback(this.RESULT_SUCCESS, buffer.slice(offset));
    });
  }

  onWriteRequest(data, offset, withoutResponse, callback) {
    const receivedStr = data.toString('utf8');
    console.log('Write request received:', receivedStr);
    try {
      const parsed = JSON.parse(receivedStr);
      fs.writeFile(SCORE_FILE_PATH, JSON.stringify(parsed, null, 2), err => {
        if (err) return callback(this.RESULT_UNLIKELY_ERROR);
        callback(this.RESULT_SUCCESS);
      });
    } catch (e) {
      console.error('Invalid JSON');
      callback(this.RESULT_UNLIKELY_ERROR);
    }
  }
}

const scoreCharacteristic = new ScoreCharacteristic();

const scoreService = new bleno.PrimaryService({
  uuid: SERVICE_UUID,
  characteristics: [scoreCharacteristic]
});

// BLE状態変化イベント
bleno.on('stateChange', state => {
  console.log(`Bluetooth state changed: ${state}`);
  if (state === 'poweredOn') {
    bleno.startAdvertising('ScoreService', [SERVICE_UUID]);
  } else {
    bleno.stopAdvertising();
  }
});

bleno.on('advertisingStart', error => {
  if (!error) {
    bleno.setServices([scoreService]);
    console.log('GATTサービス開始');
  } else {
    console.error('Advertising start error:', error);
  }
});

// BLE接続／切断はJSON読み書きのみでプロセス起動は不要
bleno.on('accept', clientAddress => {
  console.log(`Device connected: ${clientAddress}`);
});

bleno.on('disconnect', clientAddress => {
  console.log(`Device disconnected: ${clientAddress}`);
});

process.on('SIGINT', () => {
  console.log('Stopping BLE server...');
  bleno.stopAdvertising();
  process.exit();
});
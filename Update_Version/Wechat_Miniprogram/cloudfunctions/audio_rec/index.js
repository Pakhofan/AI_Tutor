// 云函数入口文件
const cloud = require('wx-server-sdk')

cloud.init()

var baidu = require('baidu-aip-sdk').speech;
var APP_ID = "24171749";
var API_KEY = "XzLbrR42sPAp9z8ZzcXC6QNS";
var SECRET_KEY = "Mz01KYKjA26T1rMzA6bYLi8RzPSHZeya";

// 云函数入口函数
exports.main = async (event, context) => {
  var client = new baidu(APP_ID, API_KEY, SECRET_KEY);
  var buffer = new Buffer.from(event.data.data);
  var res = await client.recognize(buffer,'pcm',16000,{dev_pid:1737});
  return res
}
// pages/home/home.js
var i = 0;
const record_manager = wx.getRecorderManager();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    message_in : [],
    message_out: [],
    input_tem: null,
    output_tem: '',
    recording: false,
    authed: false,
    result: null,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.get_record_auth()
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },
  getdata: function(question){
    var that = this;
    wx.request({
      url: 'http://192.168.1.101:8080/getdata',
      data:{
        question: question
      },
      success:function(res){
        that.setData({
          result: res.data
        })
        console.log(res.data);
      },
      fail:function(res){
        console.log(".....fail.....");
      }
    })
  },
  postdata: function(question){
    var that = this;
    wx.request({
      url: 'http://192.168.43.236:8080/postdata',//localhost替换成同一wifi环境下的IPv4地址，随时会变
      data:{
        question: question
      },
      success:function(res) {
        that.data.message_out.push(res.data);
        that.setData({
          message_out: that.data.message_out,
        })
      },
      fail:function(res){
        console.log("...fail...")
      }
    })
    i++;
  },
  formSubmit(e) {
    this.data.message_in.push(e.detail.value["question"]);
    console.log("in: " + this.data.message_in);
    this.postdata(e.detail.value["question"]);
    this.setData({
      message_in : this.data.message_in,
      input_tem: '',
    });
  },
  start_record: function(){
    const options={
      sampleRate: 16000,
      numberOfChannels:1,
      encodeBitRate:48000,
      format: 'PCM',
    };
    record_manager.start(options);
    this.setData({
      recording: true,
    });
  },
  stop_record: function(){
    record_manager.stop();
    this.setData({recording: false});
    this.bind_stop();
  },
  bind_stop: function(){
    var that = this;
    record_manager.onStop(res=>{
      var tf = res.tempFilePath;
      const fs = wx.getFileSystemManager();
      fs.readFile({
        filePath: tf,
        success(res){
          const buffer = res.data;
          that.audio_rec(buffer);
        }
      })
    })
  },
  audio_rec(data){
    var that = this;
    wx.showLoading({
      title: 'Recognizing',
    })
    wx.cloud.callFunction({
      name:'audio_rec',
      data: {data}
    }).then(res=>{
      if(res.errMsg=="cloud.callFunction:ok" && res.result.err_no == 0){
        var result_list = res.result.result;
        var question = result_list[0] + "?";
        that.data.message_in.push(question);
        that.setData({
          message_in : that.data.message_in,
          input_tem: '',
        });
        that.postdata(question);
        wx.hideLoading();
      }
      else{
        wx.showToast({
          title: '识别失败',
          icon: 'none',
        })
      }
    }).catch(err=>{
      console.log("err",err)
      wx.showToast({
        title: '识别失败',
        icon: 'none',
      })
    })
  },
  //小程序手机录音授权
  get_record_auth: function(){
    var that = this;
    wx.getSetting().then(res=>{
      if(res.authSetting['scope.record']){
        that.setData({authed: true})
      }
      else{
        wx.authorize({
          scope: 'scope.record',
        }).then(res=>{
          that.setData({authed:true})
        }).catch(res=>{
          that.cancel_auth()
        })
      }
    })
  },
  cancel_auth: function(){
    var that = this;
    wx.showModal({
      title: "提示",
      content: "未授权无法录音",
      cancelText: "不录音",
      confirmText: "去授权",
      success:res=>{
        if(res.confirm){
          wx.openSetting({
            success(res){
              if(res.authSetting['scope_record']){
                that.setData({
                  authed: true,
                })
              }
            }
          })
        }
      }
    })
  },
})
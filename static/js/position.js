
function getLocation()
  {
      var mypt=document.getElementById("myposition");
  if (navigator.geolocation)
    {
    navigator.geolocation.getCurrentPosition(showPosition);
    }
  else{mypt.innerHTML="该浏览器不支持获取地理位置。";}
  }
function showPosition(position)
  {
      var mypt=document.getElementById("myposition");
  mypt.innerHTML="纬度: " + position.coords.latitude +
  "<br>经度: " + position.coords.longitude;


  var lldata={
    "jingdu": position.coords.longitude,
    "weidu" : position.coords.latitude
  };

  $.ajax({
                    url: '/sign_in',
                    type: 'POST',
                    dataType: 'json',
                    data:JSON.stringify(lldata) ,
                    contentType:'application/json',
                    success:function () {
                        alert("签到成功！");
                    },
                    error:function () {
                        alert("签到失败！");
                    }
                })

  }



  function sign_in() {
        fnDate();
        changezt();
        getLocation();
  }


























  function getLocation2()
  {
      var mypt2=document.getElementById("myposition2");
  if (navigator.geolocation)
    {
    navigator.geolocation.getCurrentPosition(showPosition2);
    }
  else{mypt.innerHTML="该浏览器不支持获取地理位置。";}
  }
function showPosition2(position)
  {
      var mypt2=document.getElementById("myposition2");
  mypt2.innerHTML="纬度: " + position.coords.latitude +
  "<br>经度: " + position.coords.longitude;



          var lldata2={
            "jingdu": position.coords.longitude,
            "weidu" : position.coords.latitude
          };

          $.ajax({
                            url: '/sign_out',
                            type: 'POST',
                            dataType: 'json',
                            data:JSON.stringify(lldata2) ,
                            contentType:'application/json',
                            success:function () {
                                alert("签退成功！");
                            },
                            error:function () {
                                alert("签退失败！");
                            }
                        })
  }






    function sign_out() {
        fnDate2();
        changezt2();
        getLocation2();
  }
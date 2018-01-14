// ==UserScript==
// @name           答题助手
// @author         石头
// @match          *://xxjs.dtdjzx.gov.cn/kaishijingsai*
// @namespace      https://github.com/shichengcn/shichengcn.github.io/tree/master/party_building_automatic_answer
// @version        0.1
// @description    [答题助手][自动答题]
// @license        MIT
// @supportURL     https://github.com/shichengcn/shichengcn.github.io/issues
// @date           01/11/2018
// @modified       01/12/2018
// ==/UserScript==

var daoshushjian = 120; 

function daan(){
    ajax2('game_info/lookBackSubject',{roundOnlyId:roundOnlyId});
	$.ajax({
          async:false ,
          type: "post",
          url:oUrls+'game_info/lookBackSubject',
          data:{roundOnlyId:roundOnlyId},
          dataType: "json",
          success: function(data) {
              ubjectInfoList=[];
              //console.log(w_total);
              console.log(data);
              for(var i=0; i<w_total;i++){
                  w_jjson={};
                  //w_jjson.id=$('[name="ra_'+i+'"]:checked').attr('ids');
                  //w_jjson.answer=$('[name="ra_'+i+'"]:checked').val();
                  w_jjson.id = data.data.dateList[i].subjectId;
                  w_jjson.answer = data.data.dateList[i].answer;
                  subjectInfoList.push(w_jjson);
              }
              localStorage.setItem('allData20',JSON.stringify(subjectInfoList)); //答案缓存
              subjectInfoList=[];
          }
        });
}

function atuo_ans(){
    daan();
    var subjectInfoList = JSON.parse(localStorage.getItem("allData20")); //获取答案缓存
     //console.log($('.W_ti_ul li div input'));
    //console.log(subjectInfoList);
    var j = 0;
     for(var i=0; i<$('.W_ti_ul li div input').length;i=i+4){

         for(var k=0; k<w_total;k++){
             if($('.W_ti_ul li div input')[i].attributes.ids.value == subjectInfoList[k].id){
                 ans_str = subjectInfoList[k].answer;
                 //console.log($('.W_ti_ul li div input')[i].attributes.ids.value);
                 //console.log(subjectInfoList[k].id);
             }

         }

        //ans_str = subjectInfoList[j].answer;
        //console.log(subjectInfoList[j].answer);
        //console.log($('.W_ti_ul li div input')[i].attributes.ids.value);
        //console.log(ans_str);
        j = j+1;
        if(ans_str.indexOf("A") >= 0){
            $('.W_ti_ul li div input')[i].checked = true;
        }
        if(ans_str.indexOf("B") >= 0){
            $('.W_ti_ul li div input')[i+1].checked = true;
        }
        if(ans_str.indexOf("C") >= 0){
            $('.W_ti_ul li div input')[i+2].checked = true;
        }
        if(ans_str.indexOf("D") >= 0){
            $('.W_ti_ul li div input')[i+3].checked = true;
        }
        $('.W_kuan li').eq(j).addClass('activess');
     }
    $("body > div.l_box > div > div.w_loads > div > ul > li:nth-child(1)").addClass('activess');
    $('.W_kuan li').eq(j+1).addClass('activess');
    w_nowNum = w_total-1;
    localStorage.setItem('anniujia',w_nowNum);
    $('.w_btn_tab_down').removeClass('W_bgcol');
    subjectInfoList=[];

}

var mytime = 0;
var myjisiqi=setInterval(daojishi,1000);
function daojishi(){
	mytime++;
	if(parseInt(mytime)< parseInt(daoshushjian)){
		$(".W_jiaoquancol")["0"].innerText = "交卷倒计时:" + (parseInt(daoshushjian) - parseInt(mytime)) + "秒";
         $('.jiaojuanss').addClass('W_jiaoquancol');
	}else{
        if( w_nowNum == w_total-1){
           //console.log("检测到全部答完");
            $(".W_jiaoquancol")["0"].innerText = "交卷";
            window.clearInterval(myjisiqi);
           $('.jiaojuanss').removeClass('W_jiaoquancol')	;
            //jiaojuan();
            //iaojuan();
             //var subjectInfoList = JSON.parse(localStorage.getItem("allData2")); //获取答案缓存
            //w_chuanzou.recordId=recordId;
           // w_chuanzou.roundOnlyId=roundOnlyId;
            //w_chuanzou.subjectInfoList=subjectInfoList;
            //w_chuanzou.orderId=orderId;
            //subjectInfoList=[];
            //ajax4('chapter_info/countScore',w_chuanzou);
           //ajax4('chapter_info/countScore',w_chuanzou);
           // w_chuanzou={};
        }
	}

}
atuo_ans();
